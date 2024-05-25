from unittest.mock import Mock

from hypernode_api_python.commands import print_response
from tests.testcase import TestCase


class TestPrintResponse(TestCase):
    def setUp(self):
        self.response = Mock()
        self.response.json.return_value = {
            "id": 123,
            "code": "sla-standard",
            "name": "SLA Standard",
            "price": 1234,
            "billing_period": 1,
            "billing_period_unit": "month",
        }

        self.print = self.set_up_patch("hypernode_api_python.commands.print")

    def test_print_response_prints_pretty_response(self):
        print_response(self.response)

        self.print.assert_called_once_with(
            '{\n  "id": 123,\n  "code": "sla-standard",\n  "name": "SLA Standard",\n  '
            '"price": 1234,\n  "billing_period": 1,\n  "billing_period_unit": "month"\n}'
        )

    def test_print_response_returns_none(self):
        ret = print_response(self.response)

        self.assertIsNone(ret)
