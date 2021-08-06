import unittest
from mock import patch
from unittest.mock import MagicMock
from barely.plugins.content.Minify.minify import Minify


class TestMinify(unittest.TestCase):

    def test___init__(self):
        mini = Minify()
        self.assertDictEqual({"PRIORITY": -1}, mini.plugin_config)
        self.assertListEqual([], mini.register_for)

        golden = {
            "PRIORITY": 2,
            "JS_OBFUSCATE": True,
            "JS_OBFUSCATE_GLOBALS": True,
            "CSS_INCLUDE_COMMENTS": False,
            "CSS_OUTPUT_STYLE": "compressed"
        }

        golden_register_for = ["js", "sass", "scss"]

        mini.config["MINIFY"] = {"PRIORITY": 2}
        mini.__init__()

        self.assertDictEqual(golden, mini.plugin_config)
        self.assertListEqual(golden_register_for, mini.register_for)

        # reset
        del mini.config["MINIFY"]
        mini.__init__()

    def test_register(self):
        mini = Minify()
        name, prio, ext = mini.register()

        self.assertEqual(name, "Minify")
        self.assertEqual(prio, -1)
        self.assertEqual(ext, [])

    @patch("barely.plugins.content.Minify.minify.minify_print")
    @patch("barely.plugins.content.Minify.minify.es5")
    @patch("barely.plugins.content.Minify.minify.sass")
    def test_action(self, sass, es5, minifyjs):
        sass.compile = MagicMock(return_value="compiled")
        minifyjs.return_value = "smallerjs"

        item = {
            "destination": "",
            "output": "",
            "extension": "",
            "content_raw": ""
        }

        mini = Minify()
        mini.config["MINIFY"] = {"PRIORITY": 1}
        mini.__init__()

        # SASS
        item["destination"] = "style.sass"
        item["extension"] = "sass"
        result = list(mini.action(item=item.copy()))[0]
        self.assertEqual(result["destination"], "style.css")
        self.assertEqual(result["output"], "compiled")
        self.assertEqual(result["action"], "compiled")

        # JS
        item["extension"] = "js"
        result = list(mini.action(item=item.copy()))[0]
        self.assertEqual(result["output"], "smallerjs")
        self.assertEqual(result["action"], "compiled")

        del mini.config["MINIFY"]
        mini.__init__()
