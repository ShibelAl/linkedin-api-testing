from infra.config_provider import ConfigProvider


class ProfileAPIs:

    def __init__(self, request):
        """
        Initializes the ProfileAPIs class with a request object and loads configuration.

        :param request: The request object to handle HTTP requests.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()

    def get_profile_data_by_url(self):
        """
        Makes the URL for a profile and makes a GET request.

        :return: (dict) The response from the GET request to the profile link endpoint.
        """
        url = f"{self._config['base_url']}/{self._config['get_profile_data_by_url_endpoint']}"
        return self._request.get_request(url, self._config['get_profile_data_by_url_headers'],
                                         self._config['get_profile_data_by_url_querystring'])

    def get_profile_data_and_connections_follower_count(self):
        """
        Makes the URL for a profile and makes a GET request.

        :return: (dict) The response from the GET request to the profile data link endpoint.
        """
        url = f"{self._config['base_url']}/{self._config['get_profile_data_and_connections_follower_count_endpoint']}"
        return self._request.get_request(url, self._config['get_profile_data_and_connections_follower_count_headers'],
                                         self._config['get_profile_data_and_connections_follower_count_querystring'])
