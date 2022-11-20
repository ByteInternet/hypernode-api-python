from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_APP_CHECK_PAYMENT_INFORMATION,
)


class TestCheckPaymentInformationForApp(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_check_app_payment_info_endpoint_is_correct(self):
        self.assertEqual(
            "/v2/app/{}/check-payment-information/",
            HYPERNODE_API_APP_CHECK_PAYMENT_INFORMATION,
        )

    def test_calls_check_app_payment_info_endpoint_properly(self):
        self.client.check_payment_information_for_app("yourhypernodeappname")

        self.mock_request.assert_called_once_with(
            "GET",
            HYPERNODE_API_APP_CHECK_PAYMENT_INFORMATION.format("yourhypernodeappname"),
        )

    def test_returns_check_app_payment_info_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.check_payment_information_for_app("yourhypernodeappname"),
            self.mock_request.return_value,
        )
