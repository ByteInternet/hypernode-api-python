from hypernode_api_python.commands import create_backup
from tests.testcase import TestCase


class TestCreateBackup(TestCase):
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

    def test_create_backup_gets_client(self):
        create_backup([])

        self.get_client.assert_called_once_with()

    def test_create_backup_gets_app_name(self):
        create_backup([])

        self.get_app_name.assert_called_once_with()

    def test_create_backup_creates_backup(self):
        create_backup([])

        self.client.create_backup.assert_called_once_with("myappname")

    def test_create_backup_prints_response(self):
        create_backup([])

        self.print_response.assert_called_once_with(
            self.client.create_backup.return_value
        )
