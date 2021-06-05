import unittest
from mock import patch
from barely.plugins.publication.sftp.sftp import SFTP


class TestSFTP(unittest.TestCase):

    def test___init__(self):
        sftp = SFTP()
        self.assertDictEqual({"PRIORITY": -1}, sftp.plugin_config)

        sftp.config["SFTP"] = {"PRIORITY": 2}
        sftp.__init__()

        golden = {
            "PRIORITY": 2,
            "HOSTNAME": "",
            "USER": "",
            "PASSWORD": "",
            "KEY": "",
            "ROOT": ""
        }

        self.assertDictEqual(golden, sftp.plugin_config)

        # reset
        del sftp.config["SFTP"]
        sftp.__init__()

    def test_register(self):
        sftp = SFTP()
        name, prio = sftp.register()

        self.assertEqual(name, "sftp")
        self.assertEqual(prio, -1)

    @patch("barely.plugins.publication.sftp.sftp.pysftp.Connection")
    def test_action(self, Connection):
        sftp = SFTP()
        sftp.plugin_config = {
            "PRIORITY": 2,
            "HOSTNAME": "",
            "USER": "",
            "PASSWORD": "",
            "KEY": "",
            "ROOT": ""
        }
        sftp.action()
        Connection.assert_called_with("", username="", password="")

        Connection.reset_mock()

        sftp.plugin_config = {
            "PRIORITY": 2,
            "HOSTNAME": "",
            "USER": "",
            "PASSWORD": "",
            "KEY": "key",
            "ROOT": ""
        }
        sftp.action()
        Connection.assert_called_with("", username="", private_key="key", private_key_pass=True)
