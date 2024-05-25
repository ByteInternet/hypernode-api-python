from hypernode_api_python.commands import get_active_products
from tests.testcase import TestCase


class TestGetActiveProducts(TestCase):
    def setUp(self):
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value

    def test_get_active_products_gets_client(self):
        get_active_products([])

        self.get_client.assert_called_once_with()

    def test_get_active_products_gets_active_products(self):
        get_active_products([])

        self.client.get_active_products.assert_called_once_with()

    def test_get_active_products_prints_active_products(self):
        get_active_products([])

        self.print_response.assert_called_once_with(
            self.client.get_active_products.return_value
        )
