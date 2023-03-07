from unittest import TestCase
from unittest.mock import Mock

from hypernode_api_python.client import (
    HYPERNODE_API_BLOCK_ATTACK_ENDPOINT,
    HypernodeAPIPython,
)


class TestBlockAttack(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="my_token")
        self.mock_request = Mock()
        self.client.requests = self.mock_request
        self.app_name = "my_app"

    def test_block_attack_endpoint_is_correct(self):
        self.assertEqual(
            "/v2/app/{}/block_attack/", HYPERNODE_API_BLOCK_ATTACK_ENDPOINT
        )

    def test_calls_block_attack_endpoint_correctly(self):
        self.client.block_attack(self.app_name, "BlockSqliBruteForce")

        self.mock_request.assert_called_once_with(
            "POST",
            f"/v2/app/{self.app_name}/block_attack/",
            data={"attack_name": "BlockSqliBruteForce"},
        )

    def test_returns_block_attack_data(self):
        response = Mock()
        response.status_code = 202
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.block_attack(self.app_name, "BlockSqliBruteForce"),
            self.mock_request.return_value,
        )
