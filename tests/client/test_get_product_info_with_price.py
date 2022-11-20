from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_PRODUCT_PRICE_DETAIL_ENDPOINT,
)


class TestGetProductInfoWithPrice(TestCase):
    def setUp(self):
        self.mock_request = Mock()
        self.client = HypernodeAPIPython(token="mytoken")
        self.client.requests = self.mock_request

    def test_calls_hypernode_api_product_endpoint_with_correct_parameters(self):
        self.client.get_product_info_with_price("MAGS")

        self.mock_request.assert_called_once_with(
            "GET", HYPERNODE_API_PRODUCT_PRICE_DETAIL_ENDPOINT.format("MAGS")
        )

    def test_returns_json_result(self):
        ret = self.client.get_product_info_with_price("MAGS")

        self.assertEqual(ret, self.mock_request.return_value)

    def test_raises_runtime_error_when_request_returns_404(self):
        self.mock_request.return_value = Mock(status_code=404)

        with self.assertRaises(RuntimeError):
            self.client.get_product_info_with_price("MAGS")

    def test_raises_specified_error_when_request_returns_404(self):
        self.mock_request.return_value = Mock(status_code=404)

        with self.assertRaises(OSError):
            self.client.get_product_info_with_price("MAGS", error_to_raise=OSError)
