from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_APP_FLOWS_ENDPOINT,
)


class TestGetFlows(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_flows_endpoint_is_correct(self):
        self.assertEqual(
            "/logbook/v1/logbooks/{}/flows", HYPERNODE_API_APP_FLOWS_ENDPOINT
        )

    def test_calls_flows_endpoint_properly(self):
        self.client.get_flows("my_app")

        self.mock_request.assert_called_once_with(
            "GET", "/logbook/v1/logbooks/my_app/flows"
        )

    def test_returns_flows_data(self):
        self.assertEqual(
            self.client.get_flows("my_app"), self.mock_request.return_value
        )
