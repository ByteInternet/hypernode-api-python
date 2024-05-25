from os import EX_UNAVAILABLE, EX_OK

from hypernode_api_python.commands import validate_app_name
from tests.testcase import TestCase


class TestValidateAppName(TestCase):
    def setUp(self):
        self.exit = self.set_up_patch("hypernode_api_python.commands.exit")
        self.print = self.set_up_patch("hypernode_api_python.commands.print")
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value

    def test_validate_app_name_gets_client(self):
        validate_app_name(["myappname"])

        self.get_client.assert_called_once_with()

    def test_validate_app_name_validates_app_name(self):
        validate_app_name(["myappname"])

        self.client.validate_app_name.assert_called_once_with("myappname")

    def test_validate_app_name_prints_app_name_is_valid(self):
        validate_app_name(["myappname"])

        self.print.assert_called_once_with("App name 'myappname' is valid.")

    def test_validate_app_name_prints_app_name_is_invalid(self):
        self.client.validate_app_name.side_effect = RuntimeError(
            "[\"This value can only contain non-capital letters 'a' through 'z' or digits "
            '0 through 9."]'
        )

        validate_app_name(["myappname"])

        self.print.assert_called_once_with(
            "App name 'myappname' is invalid: [\"This value can only contain non-capital letters "
            "'a' through 'z' or digits 0 through 9.\"]"
        )

    def test_validate_app_name_exits_zero_when_valid(self):
        validate_app_name(["myappname"])

        self.exit.assert_called_once_with(EX_OK)

    def test_validate_app_name_exits_nonzero_when_invalid(self):
        self.client.validate_app_name.side_effect = RuntimeError

        validate_app_name(["myappname"])

        self.exit.assert_called_once_with(EX_UNAVAILABLE)
