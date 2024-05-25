from hypernode_api_python.commands import get_block_attack_descriptions
from tests.testcase import TestCase


class TestGetBlockAttackDescriptions(TestCase):
    def setUp(self):
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value

    def test_get_block_attack_descriptions_gets_client(self):
        get_block_attack_descriptions([])

        self.get_client.assert_called_once_with()

    def test_get_block_attack_descriptions_gets_slas(self):
        get_block_attack_descriptions([])

        self.client.get_block_attack_descriptions.assert_called_once_with()

    def test_get_block_attack_descriptions_prints_slas(self):
        get_block_attack_descriptions([])

        self.print_response.assert_called_once_with(
            self.client.get_block_attack_descriptions.return_value
        )
