from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
)


class TestGetAppEndpointOr404(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_get_app_endpoint_or_404_gets_endpoint(self):
        self.client._get_app_endpoint_or_404("yourhypernodeappname", "/v2/app/{}/")

        self.mock_request.assert_called_once_with(
            "GET", "/v2/app/yourhypernodeappname/"
        )

    def test_raises_runtime_error_if_hypernode_api_returns_404(self):
        response = Mock()
        response.status_code = 404
        self.mock_request.return_value = response

        with self.assertRaises(RuntimeError):
            self.client._get_app_endpoint_or_404("yourhypernodeappname", "/v2/app/{}/")

    def test_raises_specified_error_if_hypernode_api_returns_404(self):
        response = Mock()
        response.status_code = 404
        self.mock_request.return_value = response

        with self.assertRaises(OSError):
            self.client._get_app_endpoint_or_404(
                "yourhypernodeappname", "/v2/app/{}/", error_to_raise=OSError
            )

    def test_get_app_endpoint_or_404_returns_response(self):
        ret = self.client._get_app_endpoint_or_404(
            "yourhypernodeappname", "/v2/app/{}/"
        )

        self.assertEqual(ret, self.mock_request.return_value)
