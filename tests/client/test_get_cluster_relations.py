from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_APP_CLUSTER_RELATIONS,
)


class TestGetClusterRelations(TestCase):
    def setUp(self):
        self.mock_request = Mock()
        self.client = HypernodeAPIPython(token="mytoken")
        self.client.requests = self.mock_request

    def test_calls_hypernode_api_cluster_relations_endpoint_with_correct_parameters(
        self,
    ):
        self.client.get_cluster_relations("yourhypernodeappname")

        self.mock_request.assert_called_once_with(
            "GET", HYPERNODE_API_APP_CLUSTER_RELATIONS.format("yourhypernodeappname")
        )

    def test_returns_result_for_hypernode_api_cluster_relations(self):
        ret = self.client.get_cluster_relations("yourhypernodeappname")

        self.assertEqual(ret, self.mock_request.return_value)
