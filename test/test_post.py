import unittest
from infra.api_wrapper import APIWrapper
from infra.config_provider import ConfigProvider
from logic.models.search_results import SearchResults
from logic.post import Post


class TestCompany(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by loading the configuration and initializing the API wrapper.
        """
        self._config = ConfigProvider.load_config_json()
        self._api_request = APIWrapper()
        self.payload = self._config['search_post_by_keyword_payload']
        self.keyword = self.payload['keyword']
        self.first_filter = self.payload['sortBy']
        self.second_filter = self.payload['datePosted']
        self.third_filter = self.payload['start']
        self.search_results_object = SearchResults(
            self.keyword, self.first_filter, self.second_filter, self.third_filter)

    def test_jobs_appearing_by_time_order(self):
        """
        Tests that job postings are ordered from newest to oldest based on their post date.

        - Asserts that the response status code is 200.
        - Asserts that the jobs are correctly ordered by time.
        """
        # Act
        response = Post(self._api_request).search_post_by_keywords(self.search_results_object.to_dict())
        response_body = response.json()
        is_all_jobs_ordered_from_new_to_old = Post(self._api_request).is_all_jobs_ordered_from_new_to_old(response_body)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_all_jobs_ordered_from_new_to_old, "The jobs not ordered from newest to oldest")
