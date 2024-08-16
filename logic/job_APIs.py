from infra.config_provider import ConfigProvider


class JobAPIs:

    def __init__(self, request):
        """
        Initializes the JobAPIs class with a request object and loads configuration.

        :param request: The request object to handle HTTP requests.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()

    def search_jobs(self):
        """
        Constructs the URL for searching jobs and makes a GET request.

        :return: (dict) The response from the GET request to the job search endpoint.
        """
        url = f"{self._config['base_url']}/{self._config['search_jobs_endpoint']}"
        return self._request.get_request(url, self._config['get_company_jobs_headers'])

    @staticmethod
    def list_of_job_ids(response_body):
        """
        Extracts and returns a list of job IDs from the API response body.

        :param response_body: (dict) The response json body from the API containing job data.
        :return: list: A list of job IDs.
        """
        job_ids = [element["id"] for element in response_body["data"]]
        return job_ids
