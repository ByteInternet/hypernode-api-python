from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_WHITELIST_ENDPOINT,
)


class TestGetWhitelistOptions(TestCase):
    def setUp(self):
        self.mock_request = Mock()
        self.client = HypernodeAPIPython(token="mytoken")
        self.client.requests = self.mock_request

    def test_calls_hypernode_api_whitelist_options_endpoint_with_correct_parameters(
        self,
    ):
        self.client.get_whitelist_options("yourhypernodeappname")

        self.mock_request.assert_called_once_with(
            "OPTIONS", HYPERNODE_API_WHITELIST_ENDPOINT.format("yourhypernodeappname")
        )

    def test_returns_json_result_for_hypernode_api_whitelist_options(self):
        ret = self.client.get_whitelist_options("yourhypernodeappname")

        self.assertEqual(ret, self.mock_request.return_value)
