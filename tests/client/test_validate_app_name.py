from unittest.mock import Mock

from tests.testcase import TestCase
from hypernode_api_python.client import (
    HypernodeAPIPython,
    HYPERNODE_API_VALIDATE_APP_NAME_ENDPOINT,
)


class TestValidateAppName(TestCase):
    def setUp(self):
        self.mock_request = Mock()
        self.client = HypernodeAPIPython(token="mytoken")
        self.client.requests = self.mock_request

    def test_hypernode_api_validate_app_name_endpoint_is_correct(self):
        self.assertEqual(
            HYPERNODE_API_VALIDATE_APP_NAME_ENDPOINT, "/v2/app/name/validate/"
        )

    def test_calls_validate_appname_endpoint_with_correct_parameters(self):
        response = Mock()
        response.content = ""
        self.mock_request.return_value = response

        self.client.validate_app_name("yourhypernodeappname")

        self.mock_request.assert_called_once_with(
            "GET",
            HYPERNODE_API_VALIDATE_APP_NAME_ENDPOINT,
            params={"name": "yourhypernodeappname"},
        )

    def test_raises_runtime_error_if_non_empty_response(self):
        with self.assertRaises(RuntimeError):
            self.client.validate_app_name("yourhypernodeappname")

    def test_raises_specified_error_if_non_empty_response_and_error_to_raise_specified(
        self,
    ):
        with self.assertRaises(OSError):
            self.client.validate_app_name(
                "yourhypernodeappname", error_to_raise=OSError
            )

    def test_raises_runtime_errors_if_json_result_is_dict(self):
        response = Mock()
        response.json.return_value = {"errors": ["fake-error"]}
        self.mock_request.return_value = response

        with self.assertRaises(RuntimeError):
            self.client.validate_app_name("yourhypernodeappname")

    def test_does_not_raise_runtime_error_if_no_content_in_response(self):
        response = Mock()
        response.content = None
        self.mock_request.return_value = response

        # Should not raise
        self.client.validate_app_name("yourhypernodeappname")

    def test_does_not_raise_runtime_error_if_empty_list_in_response(self):
        response = Mock()
        response.content.decode.return_value = "[]"
        self.mock_request.return_value = response

        # Should not raise
        self.client.validate_app_name("yourhypernodeappname")
