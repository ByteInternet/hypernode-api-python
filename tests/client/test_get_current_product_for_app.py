from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_PRODUCT_APP_DETAIL_ENDPOINT,
)


class TestGetCurrentProductForApp(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_product_app_endpoint_is_correct(self):
        self.assertEqual(
            "/v2/product/app/{}/current/", HYPERNODE_API_PRODUCT_APP_DETAIL_ENDPOINT
        )

    def test_calls_product_app_detail_endpoint_properly(self):
        self.client.get_current_product_for_app("yourhypernodeappname")

        self.mock_request.assert_called_once_with(
            "GET", "/v2/product/app/yourhypernodeappname/current/"
        )

    def test_returns_product_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.get_current_product_for_app("yourhypernodeappname"),
            self.mock_request.return_value,
        )
