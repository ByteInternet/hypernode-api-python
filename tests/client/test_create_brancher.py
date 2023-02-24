from unittest import TestCase
from unittest.mock import Mock

from hypernode_api_python.client import (
    HYPERNODE_API_BRANCHER_APP_ENDPOINT,
    HypernodeAPIPython,
)


class TestCreateBrancher(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="my_token")
        self.mock_request = Mock()
        self.client.requests = self.mock_request
        self.app_name = "my_app"

    def test_brancher_endpoint_is_correct(self):
        self.assertEqual("/v2/brancher/app/{}/", HYPERNODE_API_BRANCHER_APP_ENDPOINT)

    def test_calls_create_brancher_endpoint_properly(self):
        data = {"clear_services": ["mysql"]}
        self.client.create_brancher(self.app_name, data)

        self.mock_request.assert_called_once_with(
            "POST", f"/v2/brancher/app/{self.app_name}/", data=data
        )

    def test_returns_create_brancher_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.create_brancher(self.app_name, {}),
            self.mock_request.return_value,
        )
