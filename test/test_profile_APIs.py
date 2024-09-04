import unittest
from parameterized import parameterized
from infra.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.profile_APIs import ProfileAPIs
from infra.jira_handler import JiraHandler
from infra.test_failure_handler import TestFailureHandler


class TestProfileAPIs(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by loading the configuration and initializing the API wrapper,
        and then making a profile_APIs object, and API response.
        """
        self.jira_handler = JiraHandler()
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.profile = ProfileAPIs(self._api_request)
        self.response = self.profile.get_profile_data_by_url()

    @parameterized.expand([
        ["username", "shibel-alshech-7501b4308"], ["firstName", "Shibel"],
        ["lastName", "Alshech"], ["isCreator", False], ["isOpenToWork", False],
        ["isHiring", False], ["backgroundImage", None], ["summary", ""],
        ["headline", "Computer Science student at The Open University of Israel"]
    ])
    def test_if_user_data_is_correct(self, name, expected_data):
        """
        Test if the user data is correct.

        - Asserts that the response status code is 200.
        - Asserts that the user data is equal to the expected data
        """
        try:
            # Act
            response_body = self.response.json()
            # Assert
            self.assertEqual(self.response.status_code, 200)
            self.assertEqual(response_body[name], expected_data)
        except AssertionError:
            self.jira_handler.create_issue(self._config['jira_key'], "test_if_user_data_is_correct",
                                           "Bug in test_if_user_data_is_correct")

    @TestFailureHandler.handle_test_failure
    def test_specific_fields_in_the_API_response(self):
        """
        Tests specific fields in the JSON response:
        username, fieldOfStudy and degree.

        Uses the function "get_profile_data_and_connections_follower_count" in logic-profile_APIs.
        """
        # Act
        response_body = self.response.json()
        # Assert
        self.assertEqual(response_body['username'], self._config['username'])
        self.assertEqual(response_body['educations'][0]['fieldOfStudy'], self._config['fieldOfStudy'])
        self.assertEqual(response_body['educations'][0]['degree'], self._config['degree'])


if __name__ == '__main__':
    unittest.main()
