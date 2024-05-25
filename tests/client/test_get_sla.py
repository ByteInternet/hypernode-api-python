from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_ADDON_LIST_ENDPOINT,
)


class TestGetSla(TestCase):
    def setUp(self):
        self.mock_request = Mock()
        self.client = HypernodeAPIPython(token="mytoken")
        self.client.requests = self.mock_request

    def test_calls_hypernode_api_endpoint_with_correct_parameters(self):
        self.client.get_sla("sla-standard")

        self.mock_request.assert_called_once_with(
            "GET", HYPERNODE_API_ADDON_LIST_ENDPOINT + "sla-standard/"
        )

    def test_returns_json_result(self):
        ret = self.client.get_sla("sla-standard")

        self.assertEqual(ret, self.mock_request.return_value)
