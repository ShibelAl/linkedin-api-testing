import unittest
from infra.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.contact_API import ContactAPI
from infra.jira_handler import JiraHandler
from infra.test_failure_handler import TestFailureHandler


class TestContactAPI(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by loading the configuration and initializing the API wrapper,
        and then making a contact_API object and its API response.
        """
        self.jira_handler = JiraHandler()
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.contact = ContactAPI(self._api_request)
        self.response = self.contact.get_email_address()

    @TestFailureHandler.handle_test_failure
    def test_user_did_not_provide_email(self):
        """
        Tests that the user did not provide an email.

        - Asserts that the response status code is 200.
        - Asserts that the 'emails' field in the response data matches the expected value from the config.
        """
        # Act
        response_body = self.response.json()
        # Assert
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(response_body['data']['emails'], self._config['emails'])
