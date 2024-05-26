from os import EX_UNAVAILABLE, EX_OK

from hypernode_api_python.commands import destroy_brancher
from tests.testcase import TestCase


class TestDestroyBrancher(TestCase):
    def setUp(self):
        self.exit = self.set_up_patch("hypernode_api_python.commands.exit")
        self.print = self.set_up_patch("hypernode_api_python.commands.print")
        self.print_response = self.set_up_patch(
            "hypernode_api_python.commands.print_response"
        )
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value

    def test_destroy_brancher_gets_client(self):
        destroy_brancher(["myappname-eph1234"])

        self.get_client.assert_called_once_with()

    def test_destroy_brancher_destroys_brancher(self):
        destroy_brancher(["myappname-eph1234"])

        self.client.destroy_brancher.assert_called_once_with("myappname-eph1234")

    def test_destroy_brancher_prints_app_name_is_valid(self):
        destroy_brancher(["myappname-eph1234"])

        self.print.assert_called_once_with(
            "A job has been posted to cancel the 'myappname-eph1234' brancher app."
        )

    def test_destroy_brancher_prints_app_name_is_invalid(self):
        self.client.destroy_brancher.side_effect = MemoryError("Killed")

        destroy_brancher(["myappname-eph1234"])

        self.print.assert_called_once_with(
            "Brancher app 'myappname-eph1234' failed to be cancelled: Killed"
        )

    def test_destroy_brancher_exits_zero_when_cancel_job_posted(self):
        destroy_brancher(["myappname-eph1234"])

        self.exit.assert_called_once_with(EX_OK)

    def test_destroy_brancher_exits_nonzero_when_unexpected_exception_occurs(self):
        self.client.destroy_brancher.side_effect = RuntimeError

        destroy_brancher(["myappname-eph1234"])

        self.exit.assert_called_once_with(EX_UNAVAILABLE)
