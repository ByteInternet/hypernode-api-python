from hypernode_api_python.commands import get_eav_description
from tests.testcase import TestCase


class TestGetEavDescription(TestCase):
    def setUp(self):
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value

    def test_get_eav_description_gets_client(self):
        get_eav_description([])

        self.get_client.assert_called_once_with()

    def test_get_eav_description_gets_slas(self):
        get_eav_description([])

        self.client.get_app_eav_description.assert_called_once_with()

    def test_get_eav_description_prints_slas(self):
        get_eav_description([])

        self.print_response.assert_called_once_with(
            self.client.get_app_eav_description.return_value
        )
