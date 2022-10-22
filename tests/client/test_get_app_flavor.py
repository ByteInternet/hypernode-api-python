from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_APP_FLAVOR_ENDPOINT,
)


class TestGetAppFlavor(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_app_flavor_endpoint_is_correct(self):
        self.assertEqual("/v2/app/{}/flavor/", HYPERNODE_API_APP_FLAVOR_ENDPOINT)

    def test_calls_app_flavor_endpoint_propertly(self):
        self.client.get_app_flavor("my_app")

        self.mock_request.assert_called_once_with("GET", "/v2/app/my_app/flavor/")

    def test_returns_app_flavor_data(self):
        self.assertEqual(
            self.client.get_app_flavor("my_app"), self.mock_request.return_value
        )
