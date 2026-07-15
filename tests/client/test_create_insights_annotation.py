from unittest import TestCase
from unittest.mock import Mock

from hypernode_api_python.client import (
    HYPERNODE_API_INSIGHTS_ANNOTATION_CREATE_ENDPOINT,
    HypernodeAPIPython,
)


class TestCreateInsightsAnnotation(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="my_token")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_insights_annotation_create_endpoint_is_correct(self):
        self.assertEqual(
            "/v2/insights-annotation/create/",
            HYPERNODE_API_INSIGHTS_ANNOTATION_CREATE_ENDPOINT,
        )

    def test_calls_create_insights_annotation_endpoint_properly(self):
        data = {
            "name": "Deployed release 1.2.3",
            "x_axis": 1756384957,
            "app": "my_app",
            "metrics": "memory_usage",
        }
        self.client.create_insights_annotation(data)

        self.mock_request.assert_called_once_with(
            "POST", "/v2/insights-annotation/create/", data=data
        )

    def test_returns_create_insights_annotation_response(self):
        response = Mock()
        response.status_code = 201
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.create_insights_annotation({}),
            self.mock_request.return_value,
        )
