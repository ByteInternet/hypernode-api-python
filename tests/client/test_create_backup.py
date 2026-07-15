from unittest import TestCase
from unittest.mock import Mock

from hypernode_api_python.client import (
    HYPERNODE_API_BACKUPS_ENDPOINT,
    HypernodeAPIPython,
)


class TestCreateBackup(TestCase):
    def setUp(self):
        self.client = HypernodeAPIPython(token="my_token")
        self.mock_request = Mock()
        self.client.requests = self.mock_request
        self.app_name = "my_app"

    def test_backups_endpoint_is_correct(self):
        self.assertEqual("/v2/app/{}/backup/", HYPERNODE_API_BACKUPS_ENDPOINT)

    def test_calls_create_backup_endpoint_properly(self):
        self.client.create_backup(self.app_name)

        self.mock_request.assert_called_once_with(
            "POST", f"/v2/app/{self.app_name}/backup/"
        )

    def test_returns_create_backup_response(self):
        response = Mock()
        response.status_code = 200
        self.mock_request.return_value = response

        self.assertEqual(
            self.client.create_backup(self.app_name),
            self.mock_request.return_value,
        )
