import unittest
from infra.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.job_APIs import JobAPIs
from infra.jira_handler import JiraHandler
from infra.test_failure_handler import TestFailureHandler


class TestCompany(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by loading the configuration and initializing the API wrapper,
        and then making a JobAPIs object, its API response and its json body.
        """
        self.jira_handler = JiraHandler()
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.job = JobAPIs(self._api_request)
        self.response = self.job.search_jobs()
        self.response_body = self.response.json()

    @TestFailureHandler.handle_test_failure
    def test_unique_job_ids(self):
        """
        Tests that all job IDs in the job search response are unique.

        - Asserts that the response status code is 200.
        - Asserts that all job IDs are unique by comparing the number of IDs with
          the number of unique IDs (using a set).
        """
        # Act
        job_ids_list = self.job.list_of_job_ids(self.response_body)
        # Assert
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(len(job_ids_list), len(set(job_ids_list)))
