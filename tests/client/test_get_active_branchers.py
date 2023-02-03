from unittest import TestCase
from unittest.mock import Mock

from hypernode_api_python.client import (
    HYPERNODE_API_APP_BRANCHER_ENDPOINT,
    HypernodeAPIPython,
)


class TestGetActiveBranchers(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="my_token")
        self.mock_request = Mock()
        self.client.requests = self.mock_request
        self.app_name = "my_app"

    def test_brancher_endpoint_is_correct(self):
        self.assertEqual("/v2/app/{}/brancher/", HYPERNODE_API_APP_BRANCHER_ENDPOINT)

    def test_calls_get_active_branchers_endpoint_properly(self):
        self.client.get_active_branchers(self.app_name)

        self.mock_request.assert_called_once_with(
            "GET", f"/v2/app/{self.app_name}/brancher/"
        )

    def test_returns_active_branchers_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.get_active_branchers(self.app_name),
            self.mock_request.return_value,
        )
