import json

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger
from python_sdk_remote.utilities import our_get_env
from python_sdk_remote.http_response import create_authorization_http_headers

# TODO We prefer to use the endpoint_url from api_type_table
YELP_API_ENDPOINT_URL = 'https://api.yelp.com/v3/graphql'
YELP_API_KEY = our_get_env("YELP_API_KEY")
# TODO: move to consts
DEFAULT_TOTAL_ENTRIES = 10
YELP_LOCAL_COMPONENT_ID = 156
YELP_LOCAL_COMPONENT_NAME = "Local yelp importer"
DEVELOPER_EMAIL = "akiva.s@circ.zone"
LOGGER_CODE_OBJECT = {"component_id": YELP_LOCAL_COMPONENT_ID,
                      "component_name": YELP_LOCAL_COMPONENT_NAME,
                      'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
                      'developer_email': DEVELOPER_EMAIL}


class YelpImporter(metaclass=MetaLogger, object=LOGGER_CODE_OBJECT):
    def get_data(self, business_type: str, location: str, total_entries: int = DEFAULT_TOTAL_ENTRIES) -> json:

        query = gql('''
          query ($term: String!, $location: String!, $limit: Int!, $offset: Int!) {
            search(term: $term, location: $location, limit: $limit, offset: $offset) {
              business {
                name
                rating
                location {
                  address1
                  city
                  state
                  country
                  postal_code
                }
                phone
                photos
                coordinates {
                  latitude
                  longitude
                }
                hours {
                  hours_type
                  is_open_now
                  open {
                    day
                    is_overnight
                    end
                    start
                  }
                }
              }
              total
            }
          }
        ''')

        # Define GraphQL transport
        # TODO Comment the bellow call and add a call to api_management.direct
        transport = RequestsHTTPTransport(
            url=YELP_API_ENDPOINT_URL,
            headers=create_authorization_http_headers(YELP_API_KEY),
            use_json=True,
        )

        # Define GraphQL client
        graphql_client = Client(
            transport=transport,
            fetch_schema_from_transport=False,
        )

        max_per_iteration = 50
        offset = 0
        data = {"results": []}

        while offset < total_entries:
            limit = min(max_per_iteration, total_entries - offset)
            # TODO We should add the API Management In Direct
            response = graphql_client.execute(query, variable_values={
                'term': business_type, 'location': location, 'limit': limit, 'offset': offset})
            for business in response['search']['business']:
                self.logger.info(object={"Business_dict": business})
                dictionary = dict()
                # reformat dictionary to fit generic template
                dictionary["name"] = business["name"]
                dictionary["location"] = {"coordinates": business["coordinates"],
                                          "address_local_language": business["location"]["address1"],
                                          "city": business["location"]["city"],
                                          "country": business["location"]["country"],
                                          "postal_code": business["location"]["postal_code"]
                                          }
                dictionary["phone"] = {"number_original": business["phone"]},
                dictionary["storage"] = {"path": business["photos"]},
                dictionary["reaction"] = {"value": business["rating"], "reaction_type": "Rating"},
                dictionary["operational_hours"] = []
                if len(business["hours"]) > 0:
                    for day_dict in business["hours"][0]["open"]:
                        dictionary["operational_hours"].append(
                            {"day_of_week": day_dict["day"], "from": self.reformat_time_string(day_dict["start"]),
                             "until": self.reformat_time_string(day_dict["end"])})

                data["results"].append(dictionary)

            offset += limit
            total_entries = min(total_entries, response['search']['total'])
            self.logger.info(f"Retrieved data for {offset} businesses so far")

        data_json = json.dumps(data, ensure_ascii=False)
        return data_json

    # TODO: We insert a profile into the database
    #  and we send the profile_id to the importer to record what is the source of this profile
    # def insert_profile_and_update_importer(self, conn = connect()):
    # entity_id = profile generic package
    # TODO Use importer package
    #   my_importer = importer.Importer("Yelp.com GraphQL", 1)

    #   my_importer.insert_record_data_source(
    #           "United States", "Business Profile", entity_id, "https://api.yelp.com/v3/graphql")

    # TODO Let's move this to python-sdk repo time.py
    @staticmethod
    def reformat_time_string(input_str: str) -> str:
        hours = input_str[:2]
        minutes = input_str[2:]
        time_format = f"{hours}:{minutes}:00:00"
        return time_format
