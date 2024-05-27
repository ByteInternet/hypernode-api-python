from hypernode_api_python.commands import get_slas
from tests.testcase import TestCase


class TestGetSlas(TestCase):
    def setUp(self):
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value

    def test_get_slas_gets_client(self):
        get_slas([])

        self.get_client.assert_called_once_with()

    def test_get_slas_gets_slas(self):
        get_slas([])

        self.client.get_slas.assert_called_once_with()

    def test_get_slas_prints_slas(self):
        get_slas([])

        self.print_response.assert_called_once_with(self.client.get_slas.return_value)
