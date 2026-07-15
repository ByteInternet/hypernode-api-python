from hypernode_api_python.commands import delete_whitelist_rule
from tests.testcase import TestCase


class TestDeleteWhitelistRule(TestCase):
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

    def test_delete_whitelist_rule_gets_client(self):
        with self.assertRaises(SystemExit):
            delete_whitelist_rule(["1.2.3.4"])

        self.get_client.assert_called_once_with()

    def test_delete_whitelist_rule_gets_app_name(self):
        with self.assertRaises(SystemExit):
            delete_whitelist_rule(["1.2.3.4"])

        self.get_app_name.assert_called_once_with()

    def test_delete_whitelist_rule_deletes_whitelist_rule_with_default_type(self):
        with self.assertRaises(SystemExit):
            delete_whitelist_rule(["1.2.3.4"])

        expected_data = {"ip": "1.2.3.4", "type": "database"}
        self.client.delete_whitelist_rule.assert_called_once_with(
            "myappname", data=expected_data
        )

    def test_delete_whitelist_rule_deletes_whitelist_rule_with_specified_type(self):
        with self.assertRaises(SystemExit):
            delete_whitelist_rule(["1.2.3.4", "--type", "waf"])

        expected_data = {"ip": "1.2.3.4", "type": "waf"}
        self.client.delete_whitelist_rule.assert_called_once_with(
            "myappname", data=expected_data
        )

    def test_delete_whitelist_rule_exits_zero_on_success(self):
        with self.assertRaises(SystemExit) as cm:
            delete_whitelist_rule(["1.2.3.4"])

        self.assertEqual(cm.exception.code, 0)

    def test_delete_whitelist_rule_exits_nonzero_when_delete_fails(self):
        self.client.delete_whitelist_rule.side_effect = RuntimeError("some error")

        with self.assertRaises(SystemExit) as cm:
            delete_whitelist_rule(["1.2.3.4"])

        self.assertNotEqual(cm.exception.code, 0)
