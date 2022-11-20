from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_PRODUCT_LIST_ENDPOINT,
)


class TestGetActiveProducts(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_product_endpoint_is_correct(self):
        self.assertEqual("/v2/product/", HYPERNODE_API_PRODUCT_LIST_ENDPOINT)

    def test_calls_product_list_endpoint_properly(self):
        self.client.get_active_products()

        self.mock_request.assert_called_once_with("GET", "/v2/product/")

    def test_returns_product_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.get_active_products(), self.mock_request.return_value
        )
