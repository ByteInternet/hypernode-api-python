from unittest import TestCase
from unittest.mock import Mock

from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_BRANCHER_ENDPOINT,
)


class TestDestroyBrancher(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="my_token")
        self.mock_request = Mock()
        self.client.requests = self.mock_request
        self.brancher_name = "app-branchermobyname"

    def test_brancher_endpoint_is_correct(self):
        self.assertEqual("/v2/brancher/{}/", HYPERNODE_API_BRANCHER_ENDPOINT)

    def test_calls_destroy_brancher_endpoint_properly(self):
        self.client.destroy_brancher(self.brancher_name)

        self.mock_request.assert_called_once_with(
            "DELETE", HYPERNODE_API_BRANCHER_ENDPOINT.format(self.brancher_name)
        )

    def test_returns_destroy_brancher_data(self):
        response = Mock()
        response.status_code = 204
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.destroy_brancher(self.brancher_name),
            self.mock_request.return_value,
        )
