from hypernode_api_python.commands import get_sla
from tests.testcase import TestCase


class TestGetSla(TestCase):
    def setUp(self):
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value

    def test_get_sla_gets_client(self):
        get_sla(["sla-standard"])

        self.get_client.assert_called_once_with()

    def test_get_sla_gets_sla(self):
        get_sla(["sla-standard"])

        self.client.get_sla.assert_called_once_with("sla-standard")

    def test_get_sla_prints_sla(self):
        get_sla(["sla-standard"])

        self.print_response.assert_called_once_with(self.client.get_sla.return_value)
