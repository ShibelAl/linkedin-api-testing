from infra.config_provider import ConfigProvider
from logic.models.company_jobs import CompanyJobs


class Company:
    """
    This class represents a company and its job-related operations.

    Attributes:
    - request: The request object to handle HTTP requests.
    - config: The configuration loaded from the JSON file.
    """
    GET_COMPANY_JOBS_ENDPOINT = "/company-jobs"

    def __init__(self, request):
        """
        Initializes the Company class with a request object and loads configuration.

        :param request: The request object to handle HTTP requests.
        """
        self._request = request
        self._config = ConfigProvider().load_config_json()

    def get_company_job_by_body(self, comp_job):
        """
        Sends a POST request to retrieve company job data.

        :param comp_job: The payload to be sent in the POST request.
        :return: The response from the POST request.
        """
        url = f"{self._config['base_url']}{self.GET_COMPANY_JOBS_ENDPOINT}"
        return self._request.post_request(url, self._config['get_company_jobs_headers'], comp_job)

    def get_company_object(self):
        """
        Creates a dictionary payload to retrieve company jobs.

        :return: A dictionary containing the company IDs and page number.
        """
        payload = self._config['get_company_jobs_payload']
        company_ids = payload['companyIds']
        page = payload['page']
        return CompanyJobs(company_ids, page).to_dict()

    def dict_of_job_ids_and_url_endpoints(self):
        """
        Creates a dictionary mapping job IDs to the last segment of their URLs.

        :return: A dictionary where keys are job IDs and values are the last segments of URLs.
        """
        company_job_response_json = self.get_company_job_by_body(self.get_company_object()).json()

        # Making the dictionary by iterating on each item (['items'] is a list of dicts, so each item is a dictionary)
        # by doing item['url'].split('/')[-1] i'm accessing the last element in the url, which is the id in the url.
        id_url_dict = {item['id']: item['url'].split('/')[-1] for item in company_job_response_json['data']['items']}
        # Output the dictionary
        return id_url_dict

    def is_non_identical_pair(self):
        """
        Checks if there are any non-identical key-value pairs in the job ID to URL segment dictionary.

        :return: True if there is at least one key-value pair that are non-identical, False otherwise.
        """
        id_url_dict = self.dict_of_job_ids_and_url_endpoints().items()
        non_identical_pairs_list = list(filter(lambda item: item[0] != item[1], id_url_dict))

        # if non_identical_pairs is empty, is_non_identical_pair returns True.
        if non_identical_pairs_list:
            return True
        return False

    def has_all_required_fields(self):
        """
        Checks if all jobs retrieved from the API response contain all required fields.

        This method performs the following steps:
        1. Calls the API to get the company job data.
        2. Extracts the list of jobs from the API response.
        3. Retrieves the list of required fields from the configuration.
        4. Iterates through each job to ensure all required fields are present.
        5. Returns True if all jobs contain all required fields; otherwise, returns False.

        :return: bool - True if all jobs contain all required fields, False otherwise.
        """
        company_job_response_json = self.get_company_job_by_body(self.get_company_object()).json()
        jobs = company_job_response_json['data']['items']

        required_fields = self._config['job_fields']

        for job in jobs:
            for field in required_fields:
                if field not in job:
                    return False
        return True
