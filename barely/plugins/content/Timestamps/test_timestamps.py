import unittest
from mock import patch
from barely.plugins.content.Timestamps.timestamps import Timestamps


class TestTimestamps(unittest.TestCase):

    def test___init__(self):
        ts = Timestamps()
        self.assertDictEqual({"PRIORITY": -1}, ts.plugin_config)

        ts.config["TIMESTAMPS"] = {"PRIORITY": 2}
        ts.__init__()

        golden = {
            "PRIORITY": 2,
            "FORMAT": "%d.%m.%Y"
        }

        self.assertDictEqual(golden, ts.plugin_config)

        # reset
        del ts.config["TIMESTAMPS"]
        ts.__init__()

    def test_register(self):
        ts = Timestamps()
        name, prio, ext = ts.register()

        self.assertEqual(name, "Timestamps")
        self.assertEqual(prio, -1)
        self.assertEqual(ext, ["md"])

    @patch("barely.plugins.content.Timestamps.timestamps.getctime")
    @patch("barely.plugins.content.Timestamps.timestamps.getmtime")
    def test_action(self, getmtime, getctime):
        getctime.return_value = 1622928404
        getmtime.return_value = 1622928404

        ts = Timestamps()
        ts.plugin_config = {
            "PRIORITY": 3,
            "FORMAT": "%d.%m.%Y"
        }

        item = {
            "origin": "",
            "meta": {}
        }

        result = list(ts.action(item=item))[0]

        self.assertEqual(result["meta"]["created"], "05.06.2021")
        self.assertEqual(result["meta"]["edited"], "05.06.2021")

        item = {
            "origin": "",
            "meta": {
                "created": "custom",
                "edited": "custom"
            }
        }

        result = list(ts.action(item=item))[0]

        self.assertEqual(result["meta"]["created"], "custom")
        self.assertEqual(result["meta"]["edited"], "custom")
