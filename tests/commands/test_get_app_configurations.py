from hypernode_api_python.commands import get_app_configurations
from tests.testcase import TestCase


class TestGetAppConfigurations(TestCase):
    def setUp(self):
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value

    def test_get_app_configurations_gets_client(self):
        get_app_configurations([])

        self.get_client.assert_called_once_with()

    def test_get_app_configurations_gets_slas(self):
        get_app_configurations([])

        self.client.get_app_configurations.assert_called_once_with()

    def test_get_app_configurations_prints_slas(self):
        get_app_configurations([])

        self.print_response.assert_called_once_with(
            self.client.get_app_configurations.return_value
        )
