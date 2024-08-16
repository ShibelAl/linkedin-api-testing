from infra.config_provider import ConfigProvider
from datetime import datetime


class Post:
    def __init__(self, request):
        """
        Initializes the Post class with a request object and loads configuration.

        :param request: The request object to handle HTTP requests.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()

    def search_post_by_keywords(self, keywords):
        """
        Sends a POST request to retrieve search results.

        :return: The response from the POST request.
        """
        url = f"{self._config['base_url']}/{self._config['search_post_by_keyword_endpoint']}"
        return self._request.post_request(url, self._config['search_post_by_keyword_headers'], keywords)

    @staticmethod
    def is_all_jobs_ordered_from_new_to_old(json_response):
        """
        Checks if the jobs in the JSON response are ordered from newest to oldest based on their posted dates.
        :param json_response: the json body of the API response
        :return: True if the jobs dates are sorted from the newest job to the oldest.
        """
        try:
            items = json_response['data']['items']
            format_str = "%Y-%m-%d %H:%M:%S"
            dates = [datetime.strptime(item['postedDate'][:19], format_str) for item in items]
            return (dates[i] >= dates[i + 1] for i in range(len(dates) - 1))
        except KeyError:
            return False
