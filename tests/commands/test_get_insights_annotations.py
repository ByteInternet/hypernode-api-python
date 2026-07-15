from hypernode_api_python.commands import get_insights_annotations
from tests.testcase import TestCase


class TestGetInsightsAnnotations(TestCase):
    def setUp(self):
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value

    def test_get_insights_annotations_gets_client(self):
        get_insights_annotations([])

        self.get_client.assert_called_once_with()

    def test_get_insights_annotations_gets_insights_annotations(self):
        get_insights_annotations([])

        self.client.get_insights_annotations.assert_called_once_with(params={})

    def test_get_insights_annotations_passes_pagination_params(self):
        get_insights_annotations(["--limit", "10", "--offset", "20"])

        self.client.get_insights_annotations.assert_called_once_with(
            params={"limit": 10, "offset": 20}
        )

    def test_get_insights_annotations_prints_response(self):
        get_insights_annotations([])

        self.print_response.assert_called_once_with(
            self.client.get_insights_annotations.return_value
        )
