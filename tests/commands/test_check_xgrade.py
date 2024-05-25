from hypernode_api_python.commands import check_xgrade
from tests.testcase import TestCase


class TestCheckXgrade(TestCase):
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

    def test_check_xgrade_gets_client(self):
        check_xgrade(["FALCON_S_202203"])

        self.get_client.assert_called_once_with()

    def test_check_xgrade_gets_app_name(self):
        check_xgrade(["FALCON_S_202203"])

        self.get_app_name.assert_called_once_with()

    def test_check_xgrade_gets_product_info(self):
        check_xgrade(["FALCON_S_202203"])

        self.client.check_xgrade.assert_called_once_with("myappname", "FALCON_S_202203")

    def test_check_xgrade_prints_product(self):
        check_xgrade(["FALCON_S_202203"])

        self.print_response.assert_called_once_with(
            self.client.check_xgrade.return_value
        )
