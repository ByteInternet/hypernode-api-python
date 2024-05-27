from hypernode_api_python.commands import get_client
from tests.testcase import TestCase


class TestGetClient(TestCase):
    def setUp(self):
        self.hypernode_api_python = self.set_up_patch(
            "hypernode_api_python.commands.HypernodeAPIPython"
        )
        self.expected_environment = {
            "HYPERNODE_API_TOKEN": "mytoken",
        }
        self.set_up_patch(
            "hypernode_api_python.commands.environ", self.expected_environment
        )

    def test_get_client_instantiates_client(self):
        get_client()

        self.hypernode_api_python.assert_called_once_with("mytoken")

    def test_get_client_returns_instantiated_client(self):
        ret = get_client()

        self.assertEqual(ret, self.hypernode_api_python.return_value)

    def test_get_client_raises_value_error_if_no_token(self):
        del self.expected_environment["HYPERNODE_API_TOKEN"]

        with self.assertRaises(ValueError):
            get_client()

    def test_get_client_raises_value_error_if_empty_token(self):
        self.expected_environment["HYPERNODE_API_TOKEN"] = ""

        with self.assertRaises(ValueError):
            get_client()
