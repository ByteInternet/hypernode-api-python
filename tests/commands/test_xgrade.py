from unittest.mock import Mock

from hypernode_api_python.commands import xgrade
from tests.testcase import TestCase


class TestXgrade(TestCase):
    def setUp(self):
        self.print = self.set_up_patch("hypernode_api_python.commands.print")
        self.get_client = self.set_up_patch("hypernode_api_python.commands.get_client")
        self.client = self.get_client.return_value
        self.get_app_name = self.set_up_patch(
            "hypernode_api_python.commands.get_app_name"
        )
        self.get_app_name.return_value = "myappname"
        self.client.get_xgrade_descriptions.return_value = Mock(
            json=lambda: {"FALCON_L_202203": "", "BlockDownloaderBruteForce": ""}
        )
        self.client.xgrade.return_value = Mock(content="")
        self.client.get_active_products.return_value.json.return_value = [
            {
                "code": "FALCON_L_202203",
            },
            {
                "code": "FALCON_6XL_202203",
            },
        ]

    def test_xgrade_gets_client(self):
        xgrade(["FALCON_L_202203"])

        self.get_client.assert_called_once_with()

    def test_xgrade_performs_xgrade(self):
        xgrade(["FALCON_L_202203"])

        self.client.xgrade.assert_called_once_with(
            "myappname", data={"product": "FALCON_L_202203"}
        )

    def test_xgrade_prints_output_on_success(self):
        xgrade(["FALCON_L_202203"])

        self.print.assert_called_once_with(
            "The job to xgrade Hypernode 'myappname' to product 'FALCON_L_202203' has been posted"
        )

    def test_xgrade_prints_output_on_failure(self):
        self.client.xgrade.return_value = Mock(
            content='{"product":["Object with code=FALCON_6XL_202203 does not exist."]}'
        )

        xgrade(["FALCON_6XL_202203"])

        self.print.assert_called_once_with(
            '{"product":["Object with code=FALCON_6XL_202203 does not exist."]}'
        )

    def test_xgrade_raises_on_invalid_choice(self):
        with self.assertRaises(SystemExit):
            # We get the valid choices from get_xgrade_descriptions
            xgrade(["DoesNotExist"])
