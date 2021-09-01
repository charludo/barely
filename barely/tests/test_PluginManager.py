import os
import unittest
from mock import patch
from unittest.mock import MagicMock
from barely.plugins import PluginBase
from barely.common.config import config
from barely.plugins.PluginManager import PluginManager


class SamplePlugin(PluginBase):
    def action(self, item):
        yield item

    def register(self):
        return "Base", -1, []


class TestPluginBase(unittest.TestCase):

    def test___init__(self):
        mock_config = {}
        with patch.dict(config, mock_config):
            SP = SamplePlugin()
        self.assertIsNotNone(SP.config)

    def test_register(self):
        plugin = SamplePlugin()
        registration_info = plugin.register()
        self.assertTupleEqual(("Base", -1, []), registration_info)

    def test_action(self):
        plugin = SamplePlugin()
        golden_item = {
            "test": "dict"
        }

        test_item = plugin.action(item=golden_item)

        self.assertDictEqual(golden_item, list(test_item)[0])


class TestPluginManager(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        with patch.object(PluginManager, "__init__", lambda x: None):
            self.PM = PluginManager()

        os.chdir("PluginManager")

    @classmethod
    def tearDownClass(self):
        os.chdir("..")

    @patch("barely.plugins.PluginManager.PluginManager.discover_plugins")
    def test___init__(self, discover):
        mock_config = {
            "PLUGIN_PATHS": {
                "SYS": {
                    "CONTENT": "",
                    "BACKUP": "",
                    "PUBLICATION": ""
                },
                "USER": {
                    "CONTENT": "",
                    "BACKUP": "",
                    "PUBLICATION": ""
                }
            }
        }
        with patch.dict(config, mock_config):
            PM = PluginManager()
        self.assertTrue(discover.called)
        self.assertIsNotNone(PM.plugins_content)
        self.assertIsNotNone(PM.plugins_backup)
        self.assertIsNotNone(PM.plugins_publication)

    def test_discover_plugins(self):
        # Content Plugins register with filetypes and a priority
        test_dict = self.PM.discover_plugins(["content", "empty"])

        self.assertEqual(3, len(test_dict))
        self.assertIn("md", test_dict)
        self.assertIn("pdf", test_dict)
        self.assertIn("png", test_dict)

        self.assertEqual(1, len(test_dict["md"]))
        self.assertTrue(issubclass(type(test_dict["md"][0]), PluginBase))

        self.assertEqual(2, len(test_dict["png"]))
        self.assertTrue(issubclass(type(test_dict["png"][0]), PluginBase))
        self.assertTrue(issubclass(type(test_dict["png"][1]), PluginBase))

        self.assertTrue(test_dict["png"][0].register()[0] == "P2")
        self.assertTrue(test_dict["png"][1].register()[0] == "P1")

        self.assertEqual(1, len(test_dict["pdf"]))
        self.assertTrue(issubclass(type(test_dict["pdf"][0]), PluginBase))

        # Backup/Publication Plugins only register with their class
        test_list = self.PM.discover_plugins(["other"], type_content=False)
        self.assertEqual(2, len(test_list))
        self.assertTrue(issubclass(type(test_list[0]), PluginBase))
        self.assertTrue(issubclass(type(test_list[1]), PluginBase))
        self.assertTrue(test_list[0].register()[0] == "P4")
        self.assertTrue(test_list[1].register()[0] == "P3")

    def test_hook_content(self):
        # Sample Item, to be processed by plugins registered for the "test" extension
        item = {
            "extension": "test"
        }

        # The first sample plugin returns 2 items for every input item, merely duplicating it
        sample_plugin1 = SamplePlugin()
        sample_plugin1.action = MagicMock(return_value=[item, item])

        # The second plugin is the constant 1-function
        sample_plugin2 = SamplePlugin()
        sample_plugin2.action = MagicMock(return_value=1)

        # Both plugins are "registered" for the test extension
        self.PM.plugins_content = {
            "test": [sample_plugin1, sample_plugin2]
        }

        # The hook should return two "1"s.
        returned_content = self.PM.hook_content(item)
        self.assertEqual([1, 1], returned_content)

    def test_hook_backup(self):
        sample_plugin = SamplePlugin()
        sample_plugin.action = MagicMock()

        self.PM.plugins_backup = [sample_plugin]

        self.assertFalse(sample_plugin.action.called)
        self.PM.hook_backup()
        self.assertTrue(sample_plugin.action.called)

    def test_hook_publication(self):
        sample_plugin1 = SamplePlugin()
        sample_plugin1.action = MagicMock()

        sample_plugin2 = SamplePlugin()
        sample_plugin2.action = MagicMock()

        self.PM.plugins_publication = [sample_plugin1, sample_plugin2]

        self.assertFalse(sample_plugin1.action.called)
        self.assertFalse(sample_plugin2.action.called)
        self.PM.hook_publication()
        self.assertTrue(sample_plugin1.action.called)
        self.assertTrue(sample_plugin2.action.called)
