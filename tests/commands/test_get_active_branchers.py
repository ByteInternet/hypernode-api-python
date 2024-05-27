from hypernode_api_python.commands import get_active_branchers
from tests.testcase import TestCase


class TestGetActiveBranchers(TestCase):
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

    def test_get_active_branchers_gets_client(self):
        get_active_branchers([])

        self.get_client.assert_called_once_with()

    def test_get_active_branchers_gets_app_name(self):
        get_active_branchers([])

        self.get_app_name.assert_called_once_with()

    def test_get_active_branchers_gets_active_branchers(self):
        get_active_branchers([])

        self.client.get_active_branchers.assert_called_once_with("myappname")

    def test_get_active_branchers_prints_active_branchers(self):
        get_active_branchers([])

        self.print_response.assert_called_once_with(
            self.client.get_active_branchers.return_value
        )
