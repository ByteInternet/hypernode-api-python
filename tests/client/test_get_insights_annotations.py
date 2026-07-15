from unittest import TestCase
from unittest.mock import Mock

from hypernode_api_python.client import (
    HYPERNODE_API_INSIGHTS_ANNOTATION_LIST_ENDPOINT,
    HypernodeAPIPython,
)


class TestGetInsightsAnnotations(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="my_token")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_insights_annotation_list_endpoint_is_correct(self):
        self.assertEqual(
            "/v2/insights-annotation/",
            HYPERNODE_API_INSIGHTS_ANNOTATION_LIST_ENDPOINT,
        )

    def test_calls_get_insights_annotations_endpoint_properly(self):
        self.client.get_insights_annotations()

        self.mock_request.assert_called_once_with(
            "GET", "/v2/insights-annotation/", params=None
        )

    def test_calls_get_insights_annotations_endpoint_with_pagination_params(self):
        params = {"limit": 10, "offset": 20}
        self.client.get_insights_annotations(params=params)

        self.mock_request.assert_called_once_with(
            "GET", "/v2/insights-annotation/", params=params
        )

    def test_returns_get_insights_annotations_response(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.get_insights_annotations(),
            self.mock_request.return_value,
        )
