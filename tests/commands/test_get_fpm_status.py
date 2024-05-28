from hypernode_api_python.commands import get_fpm_status
from tests.testcase import TestCase


class TestGetFPMStatus(TestCase):
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

    def test_get_fpm_status_gets_client(self):
        get_fpm_status([])

        self.get_client.assert_called_once_with()

    def test_get_fpm_status_gets_fpm_status(self):
        get_fpm_status([])

        self.client.get_fpm_status.assert_called_once_with("myappname")

    def test_get_fpm_status_prints_fpm_status(self):
        get_fpm_status([])

        self.print_response.assert_called_once_with(
            self.client.get_fpm_status.return_value
        )
