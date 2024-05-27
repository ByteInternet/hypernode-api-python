from hypernode_api_python.commands import get_whitelist_rules
from tests.testcase import TestCase


class TestGetWhitelistRules(TestCase):
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

    def test_get_whitelist_rules_gets_client(self):
        get_whitelist_rules([])

        self.get_client.assert_called_once_with()

    def test_get_whitelist_rules_gets_app_name(self):
        get_whitelist_rules([])

        self.get_app_name.assert_called_once_with()

    def test_get_whitelist_rules_gets_whitelist_rules(self):
        get_whitelist_rules([])

        self.client.get_whitelist_rules.assert_called_once_with("myappname")

    def test_get_whitelist_rules_prints_whitelist_rules(self):
        get_whitelist_rules([])

        self.print_response.assert_called_once_with(
            self.client.get_whitelist_rules.return_value
        )
