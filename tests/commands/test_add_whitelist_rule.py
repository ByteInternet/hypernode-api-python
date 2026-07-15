from hypernode_api_python.commands import add_whitelist_rule
from tests.testcase import TestCase


class TestAddWhitelistRule(TestCase):
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

    def test_add_whitelist_rule_gets_client(self):
        add_whitelist_rule(["1.2.3.4"])

        self.get_client.assert_called_once_with()

    def test_add_whitelist_rule_gets_app_name(self):
        add_whitelist_rule(["1.2.3.4"])

        self.get_app_name.assert_called_once_with()

    def test_add_whitelist_rule_adds_whitelist_rule_with_default_type(self):
        add_whitelist_rule(["1.2.3.4"])

        expected_data = {"ip": "1.2.3.4", "type": "database", "description": ""}
        self.client.add_whitelist_rule.assert_called_once_with(
            "myappname", data=expected_data
        )

    def test_add_whitelist_rule_adds_whitelist_rule_with_specified_arguments(self):
        add_whitelist_rule(
            ["1.2.3.4", "--type", "waf", "--description", "my description"]
        )

        expected_data = {
            "ip": "1.2.3.4",
            "type": "waf",
            "description": "my description",
        }
        self.client.add_whitelist_rule.assert_called_once_with(
            "myappname", data=expected_data
        )

    def test_add_whitelist_rule_prints_response(self):
        add_whitelist_rule(["1.2.3.4"])

        self.print_response.assert_called_once_with(
            self.client.add_whitelist_rule.return_value
        )
