from unittest.mock import Mock, call

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
)


class TestGetAllFlows(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request
        self.flow1 = {
            "uuid": "e1db2b60-882d-4b43-8910-ce6d38ca5393",
            "state": None,
            "name": "create_backup",
            "created_at": "2023-03-05T14:13:21Z",
            "updated_at": None,
            "progress": {"running": [], "total": 0, "completed": 0},
            "logbook": "my_app",
            "tracker": {"uuid": None, "description": None},
        }
        self.flow2 = {
            "uuid": "03bd6e10-5493-4ee8-92fc-cc429faebead",
            "state": None,
            "name": "update_node",
            "created_at": "2023-03-05T14:01:56Z",
            "updated_at": None,
            "progress": {"running": [], "total": 0, "completed": 0},
            "logbook": "my_app",
            "tracker": {
                "uuid": "0dd83d83-6b9b-4fb5-9665-79fcf8235069",
                "description": None,
            },
        }

    def test_get_all_flows_returns_flows_if_only_one_page(self):
        self.mock_request.return_value.json.return_value = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [self.flow1, self.flow2],
        }

        ret = self.client.get_all_flows("my_app")

        expected_calls = [
            call("GET", "/logbook/v1/logbooks/my_app/flows"),
            call().json(),
        ]
        self.assertEqual(expected_calls, self.mock_request.mock_calls)
        expected_results = [self.flow1, self.flow2]
        self.assertEqual(expected_results, ret)

    def test_get_all_flows_returns_flows_if_only_one_page_but_limited_results_requested(
        self,
    ):
        self.mock_request.return_value.json.return_value = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [self.flow1, self.flow2],
        }

        ret = self.client.get_all_flows("my_app", limit=1)

        expected_calls = [
            call("GET", "/logbook/v1/logbooks/my_app/flows"),
            call().json(),
        ]
        self.assertEqual(expected_calls, self.mock_request.mock_calls)
        expected_results = [self.flow1]
        self.assertEqual(expected_results, ret)

    def test_get_all_flows_returns_flows_if_more_than_one_page(self):
        self.mock_request.return_value.json.side_effect = [
            {
                "count": 101,
                "next": "https://api.hypernode.com/logbook/v1/logbooks/my_app/flows/?limit=50&offset=50",
                "previous": None,
                "results": [self.flow1, self.flow2] * 25,
            },
            {
                "count": 101,
                "next": "https://api.hypernode.com/logbook/v1/logbooks/my_app/flows/?limit=50&offset=100",
                "previous": "https://api.hypernode.com/logbook/v1/logbooks/my_app/flows/?limit=50&offset=50",
                "results": [self.flow1, self.flow2] * 25,
            },
            {
                "count": 101,
                "next": None,
                "previous": "https://api.hypernode.com/logbook/v1/logbooks/my_app/flows/?limit=50&offset=100",
                "results": [self.flow1],
            },
        ]

        ret = self.client.get_all_flows("my_app")

        expected_calls = [
            call("GET", "/logbook/v1/logbooks/my_app/flows"),
            call().json(),
            call("GET", "/logbook/v1/logbooks/my_app/flows/?limit=50&offset=50"),
            call().json(),
            call("GET", "/logbook/v1/logbooks/my_app/flows/?limit=50&offset=100"),
            call().json(),
        ]
        self.assertEqual(expected_calls, self.mock_request.mock_calls)
        expected_results = [self.flow1, self.flow2] * 50 + [self.flow1]
        self.assertEqual(expected_results, ret)

    def test_get_all_flows_returns_flows_if_more_than_one_page_but_limited_results_requested(
        self,
    ):
        self.mock_request.return_value.json.side_effect = [
            {
                "count": 101,
                "next": "https://api.hypernode.com/logbook/v1/logbooks/my_app/flows/?limit=50&offset=50",
                "previous": None,
                "results": [self.flow1, self.flow2] * 25,
            },
            {
                "count": 101,
                "next": "https://api.hypernode.com/logbook/v1/logbooks/my_app/flows/?limit=50&offset=100",
                "previous": "https://api.hypernode.com/logbook/v1/logbooks/my_app/flows/?limit=50&offset=50",
                "results": [self.flow1, self.flow2] * 25,
            },
            {
                "count": 101,
                "next": None,
                "previous": "https://api.hypernode.com/logbook/v1/logbooks/my_app/flows/?limit=50&offset=100",
                "results": [self.flow1],
            },
        ]

        ret = self.client.get_all_flows("my_app", limit=51)

        expected_calls = [
            call("GET", "/logbook/v1/logbooks/my_app/flows"),
            call().json(),
            call("GET", "/logbook/v1/logbooks/my_app/flows/?limit=50&offset=50"),
            call().json(),
        ]
        self.assertEqual(expected_calls, self.mock_request.mock_calls)
        expected_results = [self.flow1, self.flow2] * 25 + [self.flow1]
        self.assertEqual(expected_results, ret)
