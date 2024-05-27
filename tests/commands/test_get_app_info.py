from hypernode_api_python.commands import get_app_info
from tests.testcase import TestCase


class TestGetAppInfo(TestCase):
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

    def test_get_app_info_gets_client(self):
        get_app_info([])

        self.get_client.assert_called_once_with()

    def test_get_app_info_gets_app_name(self):
        get_app_info([])

        self.get_app_name.assert_called_once_with()

    def test_get_app_info_gets_app_info(self):
        get_app_info([])

        self.client.get_app_info_or_404.assert_called_once_with("myappname")

    def test_get_app_info_prints_app_info(self):
        get_app_info([])

        self.print_response.assert_called_once_with(
            self.client.get_app_info_or_404.return_value
        )
