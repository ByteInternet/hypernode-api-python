from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_APP_XGRADE_ENDPOINT,
)


class TestXGrade(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_xgrade_endpoint_is_correct(self):
        self.assertEqual("/v2/app/xgrade/{}/", HYPERNODE_API_APP_XGRADE_ENDPOINT)

    def test_calls_xgrade_endpoint_properly(self):
        data = {"test": "data"}
        self.client.xgrade("yourhypernodeappname", data)

        self.mock_request.assert_called_once_with(
            "PATCH", "/v2/app/xgrade/yourhypernodeappname/", data=data
        )

    def test_returns_xgrade_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.xgrade("yourhypernodeappname", {}),
            self.mock_request.return_value,
        )
