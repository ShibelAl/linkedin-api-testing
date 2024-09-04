import unittest
from infra.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.models.company_jobs import CompanyJobs
from logic.company import Company
from infra.jira_handler import JiraHandler
from infra.test_failure_handler import TestFailureHandler


class TestCompany(unittest.TestCase):
    FIRST_ELEMENT = 0
    FUNCTION_BUG = "Bug in the function"

    def setUp(self):
        """
        Set up the test environment by loading the configuration and initializing the API wrapper.
        """
        self.jira_handler = JiraHandler()
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.payload = self._config['get_company_jobs_payload']
        self.company_ids = self.payload['companyIds']
        self.page = self.payload['page']
        self.company_object = CompanyJobs(self.company_ids, self.page)

    @TestFailureHandler.handle_test_failure
    def test_company_response_data_structures(self):
        """
        Test if the data structure of the whole response and the data-key value is Dictionary,
        and if the items-key value is a list. If this test fails, then the other tests will fail
        because they depend on these data structures, which make this a fundamental test.

        :raises AssertionError: If any of the following conditions are not met:
            - The response status code is 200.
            - The entire response body is a dictionary.
            - The 'data' key in the response body is a dictionary.
            - The 'items' key within the 'data' dictionary is a list.
        """
        # Act
        response = Company(self._api_request).get_company_job_by_body(self.company_object.to_dict())
        company_jobs_body = response.json()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(company_jobs_body, dict)
        self.assertIsInstance(company_jobs_body['data'], dict)
        self.assertIsInstance(company_jobs_body['data']['items'], list)
        self.assertIsInstance(company_jobs_body['data']['items'][self.FIRST_ELEMENT]['company'], dict)

    @TestFailureHandler.handle_test_failure
    def test_website_page_is_not_empty(self):
        """
        Tests that the company jobs page contains at least one job.

        :raises AssertionError: If the response status code is not 200 or the job
        list is empty.
        """
        # Act
        response = Company(self._api_request).get_company_job_by_body(self.company_object.to_dict())
        company_jobs_data = response.json()["data"]["items"]

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(company_jobs_data) > 0, "There is no jobs appearing in the page")

    @TestFailureHandler.handle_test_failure
    def test_each_job_has_all_fields(self):
        """
        Verify that each job in the API response includes all required fields.

        :raises AssertionError: If the response status code is not 200 or if any job is missing required fields.
        """
        try:
            # Act
            response = Company(self._api_request).get_company_job_by_body(self.company_object.to_dict())
            each_job_has_all_fields = Company(self._api_request).has_all_required_fields()

            # Assert
            self.assertEqual(response.status_code, 200)
            self.assertTrue(each_job_has_all_fields, "There is a job that doesn't contain all the required fields")
        except AssertionError:
            jira_handler = JiraHandler()
            jira_handler.create_issue(self._config['jira_key'], "test_each_job_has_all_fields", self.FUNCTION_BUG)
            raise AssertionError("assertion error")

    @TestFailureHandler.handle_test_failure
    def test_job_url_goes_to_correct_job_id(self):
        """
        Test to verify that job URLs correspond to the correct job IDs.

        This test checks if there are any non-identical key-value pairs in the job ID to URL segment dictionary.
        It asserts that the response does not contain any incorrect URLs.

        :raises AssertionError: If there is a URL that doesn't lead to the correct job ID.
        """
        # Act
        response = Company(self._api_request).get_company_job_by_body(self.company_object.to_dict())
        response_contains_wrong_url = Company(self._api_request).is_non_identical_pair()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response_contains_wrong_url, "There is a url that doesn't lead to the correct job")


if __name__ == '__main__':
    unittest.main()
