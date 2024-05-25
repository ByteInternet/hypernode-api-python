from hypernode_api_python.commands import get_product_info
from tests.testcase import TestCase


class TestGetProductInfo(TestCase):
    def setUp(self):
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value

    def test_get_product_info_gets_client(self):
        get_product_info(["FALCON_S_202203"])

        self.get_client.assert_called_once_with()

    def test_get_product_info_gets_product_info_with_price(self):
        get_product_info(["FALCON_S_202203"])

        self.client.get_product_info_with_price.assert_called_once_with(
            "FALCON_S_202203"
        )

    def test_get_product_info_prints_product(self):
        get_product_info(["FALCON_S_202203"])

        self.print_response.assert_called_once_with(
            self.client.get_product_info_with_price.return_value
        )
