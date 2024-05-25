from hypernode_api_python.commands import get_flows
from tests.testcase import TestCase


class TestGetFlows(TestCase):
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

    def test_get_flows_gets_client(self):
        get_flows([])

        self.get_client.assert_called_once_with()

    def test_get_flows_gets_app_name(self):
        get_flows([])

        self.get_app_name.assert_called_once_with()

    def test_get_flows_gets_flows(self):
        get_flows([])

        self.client.get_flows.assert_called_once_with("myappname")

    def test_get_flows_prints_flows(self):
        get_flows([])

        self.print_response.assert_called_once_with(self.client.get_flows.return_value)
