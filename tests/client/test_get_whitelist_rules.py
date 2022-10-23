from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_WHITELIST_ENDPOINT,
)


class TestGetWhitelistRules(TestCase):
    def setUp(self):
        self.mock_request = Mock()
        self.client = HypernodeAPIPython(token="mytoken")
        self.client.requests = self.mock_request

    def test_calls_hypernode_api_whitelist_rules_endpoint_with_correct_parameters(
        self,
    ):
        self.client.get_whitelist_rules("yourhypernodeappname")

        self.mock_request.assert_called_once_with(
            "GET", HYPERNODE_API_WHITELIST_ENDPOINT.format("yourhypernodeappname"), {}
        )

    def test_calls_hypernode_api_whitelist_rules_endpoint_with_correct_parameters_if_filter_specified(
        self,
    ):
        self.client.get_whitelist_rules(
            "yourhypernodeappname", filter_data={"type": "waf"}
        )

        self.mock_request.assert_called_once_with(
            "GET",
            HYPERNODE_API_WHITELIST_ENDPOINT.format("yourhypernodeappname"),
            {"type": "waf"},
        )

    def test_returns_json_result_for_hypernode_api_whitelist_rules(self):
        ret = self.client.get_whitelist_rules("yourhypernodeappname")

        self.assertEqual(ret, self.mock_request.return_value)
