from unittest import TestCase
from unittest.mock import Mock

from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_FPM_STATUS_APP_ENDPOINT,
)


class TestGetFPMStatus(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="my_token")
        self.mock_request = Mock()
        self.client.requests = self.mock_request
        self.app_name = "my_app"

    def test_get_fpm_status_endpoint_is_correct(self):
        self.assertEqual(
            "/v2/nats/{}/hypernode.show-fpm-status",
            HYPERNODE_API_FPM_STATUS_APP_ENDPOINT,
        )

    def test_calls_fpm_status_endpoint_properly(self):
        self.client.get_fpm_status(self.app_name)

        self.mock_request.assert_called_once_with(
            "POST",
            f"/v2/nats/{self.app_name}/hypernode.show-fpm-status",
        )

    def test_returns_fpm_status_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.get_fpm_status(self.app_name),
            self.mock_request.return_value,
        )
