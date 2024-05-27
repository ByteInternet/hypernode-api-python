from hypernode_api_python.commands import get_next_best_plan_for_app
from tests.testcase import TestCase


class TestGetNextBestPlan(TestCase):
    def setUp(self):
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value
        self.get_app_name = self.set_up_patch(
            "hypernode_api_python.commands.get_app_name"
        )
        self.get_app_name.return_value = "myappname"

    def test_get_next_best_plan_for_app_gets_client(self):
        get_next_best_plan_for_app([])

        self.get_client.assert_called_once_with()

    def test_get_next_best_plan_for_app_gets_app_name(self):
        get_next_best_plan_for_app([])

        self.get_app_name.assert_called_once_with()

    def test_get_next_best_plan_for_app_gets_next_best_plan_for_app(self):
        get_next_best_plan_for_app([])

        self.client.get_next_best_plan_for_app_or_404.assert_called_once_with(
            "myappname"
        )

    def test_get_next_best_plan_for_app_prints_next_best_plan_for_app(self):
        get_next_best_plan_for_app([])

        self.print_response.assert_called_once_with(
            self.client.get_next_best_plan_for_app_or_404.return_value
        )
