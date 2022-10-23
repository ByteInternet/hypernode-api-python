from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_BACKUPS_ENDPOINT,
)


class TestGetAvailableBackupsForApp(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="mytoken")
        self.mock_request = Mock()
        self.client.requests = self.mock_request

    def test_api_available_backups_endpoint_is_correct(self):
        self.assertEqual("/v2/app/{}/backup/", HYPERNODE_API_BACKUPS_ENDPOINT)

    def test_calls_available_backups_endpoint_properly(self):
        self.client.get_available_backups_for_app("myhypernodeappname")

        self.mock_request.assert_called_once_with(
            "GET", "/v2/app/myhypernodeappname/backup/"
        )

    def test_returns_available_backups_data(self):
        self.assertEqual(
            self.client.get_available_backups_for_app("myhypernodeappname"),
            self.mock_request.return_value,
        )
