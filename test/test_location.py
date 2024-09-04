import unittest
from infra.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.location import Location
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
        self.location = Location(self._api_request)
        self.response = self.location.search_locations()
        self.response_body = self.response.json()

    @TestFailureHandler.handle_test_failure
    def test_if_locations_is_in_berlin(self):
        """
        Tests if all location names in the response contain the substring 'Berlin'.

        - Asserts that the response status code is 200.
        - Asserts that all location names contain 'Berlin'.
        """
        # Act
        all_names_contain_berlin = Location(self._api_request).all_names_contain_berlin(self.response_body)
        # Assert
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(all_names_contain_berlin)
