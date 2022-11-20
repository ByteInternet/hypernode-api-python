from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_APP_CONFIGURATION_ENDPOINT,
)


class TestGetAppConfiguration(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_api_app_configuration_list_endpoint_is_correct(self):
        self.assertEqual("/v2/configuration/", HYPERNODE_API_APP_CONFIGURATION_ENDPOINT)

    def test_calls_app_configuration_endpoint_properly(self):
        self.client.get_app_configurations()

        self.mock_request.assert_called_once_with(
            "GET", HYPERNODE_API_APP_CONFIGURATION_ENDPOINT
        )

    def test_returns_app_configuration_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.get_app_configurations(), self.mock_request.return_value
        )
