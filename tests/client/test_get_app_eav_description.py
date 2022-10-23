from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
)


class TestGetAppDescription(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_calls_hypernode_api_app_eav_description_endpoint(self):
        self.client.get_app_eav_description()

        self.mock_request.assert_called_once_with("GET", "/v2/app/eav_descriptions/")

    def test_returns_response_json_if_hypernode_api_returns_description(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        ret = self.client.get_app_eav_description()

        self.assertEqual(ret, self.mock_request.return_value)
