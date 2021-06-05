import os
import unittest
from mock import patch, call
from unittest.mock import MagicMock
from barely.plugins.backup.LocalBackup.localbackup import LocalBackup


class TestLocalBackup(unittest.TestCase):

    def test___init__(self):
        lb = LocalBackup()
        self.assertDictEqual({"PRIORITY": -1}, lb.plugin_config)

        lb.config["LOCAL_BACKUP"] = {"PRIORITY": 2}
        lb.__init__()

        golden = {
            "PRIORITY": 2,
            "MAX": 10,
            "BAKROOT": os.path.join(os.path.dirname(lb.config["ROOT"]["DEV"]), "backups")
        }

        self.assertDictEqual(golden, lb.plugin_config)

        # reset
        del lb.config["LOCAL_BACKUP"]
        lb.__init__()

    def test_register(self):
        lb = LocalBackup()
        name, prio = lb.register()

        self.assertEqual(name, "LocalBackup")
        self.assertEqual(prio, -1)

    @patch("barely.plugins.backup.LocalBackup.localbackup.glob")
    @patch("barely.plugins.backup.LocalBackup.localbackup.shutil")
    def test_action(self, shutil, glob):
        shutil.copytree = MagicMock()
        shutil.rmtree = MagicMock()

        glob.glob = MagicMock(return_value=[])

        lb = LocalBackup()
        lb.plugin_config["MAX"] = 2
        lb.plugin_config["BAKROOT"] = "backups"
        lb.action()

        self.assertTrue(shutil.copytree.called)
        self.assertTrue(shutil.rmtree.called_once)
        self.assertTrue(glob.glob.called)

        glob.glob.return_value = [1, 2, 3]
        shutil.rmtree.reset_mock()
        lb.action()
        self.assertTrue(call(3) in shutil.rmtree.call_args_list)
        self.assertTrue(call(2) in shutil.rmtree.call_args_list)

        lb.plugin_config["MAX"] = 10
