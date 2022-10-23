from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
)


class TestGetNextBestPlanForAppOr404(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_calls_hypernode_api_app_next_best_plan_endpoint_with_app_name(self):
        self.client.get_next_best_plan_for_app_or_404("yourhypernodeappname")

        self.mock_request.assert_called_once_with(
            "GET", "/v2/app/yourhypernodeappname/next_best_plan/"
        )

    def test_raises_if_hypernode_api_returns_404_for_next_best_plan_app(self):
        response = Mock()
        response.status_code = 404
        self.mock_request.return_value = response

        with self.assertRaises(RuntimeError):
            self.client.get_next_best_plan_for_app_or_404("yourhypernodeappname")

    def test_returns_response_json_if_hypernode_api_returns_next_best_plan(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        ret = self.client.get_next_best_plan_for_app_or_404("yourhypernodeappname")

        self.assertEqual(ret, self.mock_request.return_value)
