import unittest
from mock import patch
from unittest.mock import MagicMock
from barely.plugins.content.Minify.minify import Minify


class TestMinify(unittest.TestCase):

    def test___init__(self):
        mini = Minify()

        standard_config = {
            "PRIORITY": 3,
            "JS_OBFUSCATE": True,
            "JS_OBFUSCATE_GLOBALS": True,
            "CSS_INCLUDE_COMMENTS": False,
            "CSS_OUTPUT_STYLE": "compressed"
        }

        self.assertDictEqual(standard_config, mini.plugin_config)
        self.assertListEqual(["js", "sass", "scss"], mini.register_for)

    def test_register(self):
        mini = Minify()
        name, prio, ext = mini.register()

        self.assertEqual(name, "Minify")
        self.assertEqual(prio, 3)
        self.assertEqual(ext, ["js", "sass", "scss"])

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
