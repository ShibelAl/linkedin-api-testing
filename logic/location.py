from infra.config_provider import ConfigProvider


class Location:

    def __init__(self, request):
        """
        Initializes the Location class with a request object and loads configuration.

        :param request: The request object to handle HTTP requests.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()

    def search_locations(self):
        """
        Constructs the URL for searching jobs and makes a GET request.

        :return: (dict) The response from the GET request to the search location endpoint.
        """
        url = f"{self._config['base_url']}/{self._config['search_locations_endpoint']}"
        return self._request.get_request(url, self._config['search_locations_headers'],
                                         self._config['search_locations_querystring'])

    @staticmethod
    def all_names_contain_berlin(response_body):
        """
        Checks if all 'name' fields in the response data contain the substring 'Berlin'.

        :param response_body: (dict) The JSON response body containing the data.
        :return: bool: True if all names contain 'Berlin', False otherwise.
        """
        try:
            # Extract the list of items - that in this case, locations - from the response body
            items = response_body["data"]["items"]

            # Iterate over each item and check if the 'name' contains 'Berlin'
            return all("Berlin" in item["name"] for item in items)
        except KeyError:
            return False
