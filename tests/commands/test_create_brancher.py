from hypernode_api_python.commands import create_brancher
from tests.testcase import TestCase


class TestCreateBrancher(TestCase):
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

    def test_create_brancher_gets_client(self):
        create_brancher([])

        self.get_client.assert_called_once_with()

    def test_create_brancher_gets_app_name(self):
        create_brancher([])

        self.get_app_name.assert_called_once_with()

    def test_create_brancher_creates_brancher(self):
        create_brancher([])

        expected_data = {}
        self.client.create_brancher.assert_called_once_with(
            "myappname", data=expected_data
        )

    def test_create_brancher_prints_response(self):
        create_brancher([])

        self.print_response.assert_called_once_with(
            self.client.create_brancher.return_value
        )
