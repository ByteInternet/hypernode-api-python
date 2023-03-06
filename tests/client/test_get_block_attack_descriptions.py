from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_BLOCK_ATTACK_DESCRIPTION_ENDPOINT,
)


class TestGetBlockAttackDescriptions(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_block_attack_descriptions_endpoint_is_correct(self):
        self.assertEqual(
            "/v2/app/block_attack_descriptions/",
            HYPERNODE_API_BLOCK_ATTACK_DESCRIPTION_ENDPOINT,
        )

    def test_calls_block_attack_descriptions_detail_endpoint_properly(self):
        self.client.get_block_attack_descriptions()

        self.mock_request.assert_called_once_with(
            "GET", "/v2/app/block_attack_descriptions/"
        )

    def test_returns_block_attack_descriptions(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.get_block_attack_descriptions(),
            self.mock_request.return_value,
        )
