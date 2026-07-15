from hypernode_api_python.commands import create_insights_annotation
from tests.testcase import TestCase


class TestCreateInsightsAnnotation(TestCase):
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

    def test_create_insights_annotation_gets_client(self):
        create_insights_annotation(["Deployed release 1.2.3", "1756384957"])

        self.get_client.assert_called_once_with()

    def test_create_insights_annotation_gets_app_name(self):
        create_insights_annotation(["Deployed release 1.2.3", "1756384957"])

        self.get_app_name.assert_called_once_with()

    def test_create_insights_annotation_creates_annotation(self):
        create_insights_annotation(["Deployed release 1.2.3", "1756384957"])

        expected_data = {
            "name": "Deployed release 1.2.3",
            "x_axis": 1756384957,
            "app": "myappname",
        }
        self.client.create_insights_annotation.assert_called_once_with(
            data=expected_data
        )

    def test_create_insights_annotation_creates_annotation_with_optional_arguments(
        self,
    ):
        create_insights_annotation(
            [
                "Deployed release 1.2.3",
                "1756384957",
                "--metrics",
                "memory_usage",
                "--metadata",
                "some metadata",
            ]
        )

        expected_data = {
            "name": "Deployed release 1.2.3",
            "x_axis": 1756384957,
            "app": "myappname",
            "metrics": "memory_usage",
            "metadata": "some metadata",
        }
        self.client.create_insights_annotation.assert_called_once_with(
            data=expected_data
        )

    def test_create_insights_annotation_prints_response(self):
        create_insights_annotation(["Deployed release 1.2.3", "1756384957"])

        self.print_response.assert_called_once_with(
            self.client.create_insights_annotation.return_value
        )
