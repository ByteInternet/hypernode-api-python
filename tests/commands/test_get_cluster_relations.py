from hypernode_api_python.commands import get_cluster_relations
from tests.testcase import TestCase


class TestGetClusterRelations(TestCase):
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

    def test_get_cluster_relations_gets_client(self):
        get_cluster_relations([])

        self.get_client.assert_called_once_with()

    def test_get_cluster_relations_gets_app_name(self):
        get_cluster_relations([])

        self.get_app_name.assert_called_once_with()

    def test_get_cluster_relations_gets_cluster_relations(self):
        get_cluster_relations([])

        self.client.get_cluster_relations.assert_called_once_with("myappname")

    def test_get_cluster_relations_prints_cluster_relations(self):
        get_cluster_relations([])

        self.print_response.assert_called_once_with(
            self.client.get_cluster_relations.return_value
        )
