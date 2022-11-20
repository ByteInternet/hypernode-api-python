from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_APP_ORDER_ENDPOINT,
)


class TestOrderHypernode(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_order_hypernode_endpoint_is_correct(self):
        self.assertEqual("/v2/app/order/", HYPERNODE_API_APP_ORDER_ENDPOINT)

    def test_calls_order_hypernode_endpoint_properly(self):
        data = {
            "app_name": "mynewhypernodeappnameofmax16chars",
            "product": "FALCON_S_202203",
            "initial_app_configuration": "magento_2",
        }
        self.client.order_hypernode(data)

        self.mock_request.assert_called_once_with("POST", "/v2/app/order/", data=data)

    def test_returns_hypernode_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.order_hypernode({}), self.mock_request.return_value
        )
