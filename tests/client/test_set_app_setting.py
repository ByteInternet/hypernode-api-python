from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_APP_DETAIL_ENDPOINT,
)


class TestSetAppSetting(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_set_app_setting_endpoint_is_correct(self):
        self.assertEqual(
            "/v2/app/{}/?destroyed=false", HYPERNODE_API_APP_DETAIL_ENDPOINT
        )

    def test_calls_set_app_setting_endpoint_properly(self):
        self.client.set_app_setting("yourhypernodeappname", "php_version", "8.1")

        expected_data = {"php_version": "8.1"}
        self.mock_request.assert_called_once_with(
            "PATCH", "/v2/app/yourhypernodeappname/?destroyed=false", data=expected_data
        )

    def test_returns_set_app_setting_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.set_app_setting("yourhypernodeappname", "php_version", "8.1"),
            self.mock_request.return_value,
        )
