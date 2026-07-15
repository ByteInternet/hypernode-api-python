from unittest import TestCase
from unittest.mock import Mock

from hypernode_api_python.client import (
    HYPERNODE_API_WHITELIST_ENDPOINT,
    HypernodeAPIPython,
)


class TestDeleteWhitelistRule(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="my_token")
        self.mock_request = Mock()
        self.client.requests = self.mock_request
        self.app_name = "my_app"

    def test_whitelist_endpoint_is_correct(self):
        self.assertEqual("/v2/whitelist/{}/", HYPERNODE_API_WHITELIST_ENDPOINT)

    def test_calls_delete_whitelist_rule_endpoint_properly(self):
        data = {"ip": "1.2.3.4", "type": "database"}
        self.client.delete_whitelist_rule(self.app_name, data)

        self.mock_request.assert_called_once_with(
            "DELETE", f"/v2/whitelist/{self.app_name}/", data=data
        )

    def test_returns_delete_whitelist_rule_response(self):
        response = Mock()
        response.status_code = 204
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.delete_whitelist_rule(self.app_name, {"ip": "1.2.3.4"}),
            self.mock_request.return_value,
        )
