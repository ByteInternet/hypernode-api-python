from unittest.mock import Mock

from hypernode_api_python.commands import block_attack
from tests.testcase import TestCase


class TestBlockAttack(TestCase):
    def setUp(self):
        self.print = self.set_up_patch("hypernode_api_python.commands.print")
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value
        self.get_app_name = self.set_up_patch(
            "hypernode_api_python.commands.get_app_name"
        )
        self.get_app_name.return_value = "myappname"
        self.client.get_block_attack_descriptions.return_value = Mock(
            json=lambda: {"BlockSqliBruteForce": "", "BlockDownloaderBruteForce": ""}
        )
        self.client.block_attack.return_value = Mock(content="")

    def test_block_attack_gets_client(self):
        block_attack(["BlockSqliBruteForce"])

        self.get_client.assert_called_once_with()

    def test_block_attack_blocks_attack(self):
        block_attack(["BlockSqliBruteForce"])

        self.client.block_attack.assert_called_once_with(
            "myappname", "BlockSqliBruteForce"
        )

    def test_block_attack_prints_output_on_success(self):
        block_attack(["BlockSqliBruteForce"])

        self.print.assert_called_once_with(
            "A job to block the 'BlockSqliBruteForce' attack has been posted."
        )

    def test_block_attack_prints_output_on_failure(self):
        self.client.block_attack.return_value = Mock(
            content='{"attack_name":["\\"BlockDownloaderBruteForce\\" is not a valid choice."]}'
        )

        block_attack(["BlockDownloaderBruteForce"])

        self.print.assert_called_once_with(
            '{"attack_name":["\\"BlockDownloaderBruteForce\\" is not a valid choice."]}'
        )

    def test_block_attack_raises_on_invalid_choice(self):
        with self.assertRaises(SystemExit):
            # We get the valid choices from get_block_attack_descriptions
            block_attack(["DoesNotExist"])
