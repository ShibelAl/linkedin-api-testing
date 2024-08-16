from infra.config_provider import ConfigProvider


class ContactAPI:

    def __init__(self, request):
        """
        Initializes the ProfileAPIs class with a request object and loads configuration.

        :param request: The request object to handle HTTP requests.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()

    def get_email_address(self):
        """
        Makes the URL for a profile and makes a GET request.

        :return: (dict) The response from the GET request to the username linkedin-email endpoint.
        """
        url = f"{self._config['base_url']}/{self._config['find_email_address_endpoint']}"
        return self._request.get_request(url, self._config['find_email_address_headers'],
                                         self._config['find_email_address_querystring'])
