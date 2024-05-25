from hypernode_api_python.commands import get_app_name
from tests.testcase import TestCase


class TestGetAppName(TestCase):
    def setUp(self):
        self.expected_environment = {
            "HYPERNODE_APP_NAME": "myappname",
        }
        self.set_up_patch(
            "hypernode_api_python.commands.environ", self.expected_environment
        )

    def test_get_app_name_returns_app_name(self):
        ret = get_app_name()

        self.assertEqual(ret, "myappname")

    def test_get_app_name_raises_value_error_if_no_app_name(self):
        del self.expected_environment["HYPERNODE_APP_NAME"]

        with self.assertRaises(ValueError):
            get_app_name()

    def test_get_app_name_raises_value_error_if_empty_app_name(self):
        self.expected_environment["HYPERNODE_APP_NAME"] = ""

        with self.assertRaises(ValueError):
            get_app_name()
