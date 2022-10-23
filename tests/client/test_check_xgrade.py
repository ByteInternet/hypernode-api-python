from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_APP_XGRADE_CHECK_ENDPOINT,
)


class TestCheckXGrade(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_xgrade_check_endpoint_is_correct(self):
        self.assertEqual(
            "/v2/app/xgrade/{}/check/{}/", HYPERNODE_API_APP_XGRADE_CHECK_ENDPOINT
        )

    def test_calls_xgrade_check_endpoint_properly(self):
        self.client.check_xgrade("yourhypernodeappname", "MAGG201908")

        self.mock_request.assert_called_once_with(
            "GET", "/v2/app/xgrade/yourhypernodeappname/check/MAGG201908/"
        )

    def test_returns_check_xgrade_data(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.check_xgrade("yourhypernodeappname", "MAGG201908"),
            self.mock_request.return_value,
        )
