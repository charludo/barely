import unittest
from mock import patch
from unittest.mock import MagicMock
from barely.plugins.content.Minimizer.minimizer import Minimizer


class TestMinimizer(unittest.TestCase):

    def test___init__(self):
        mini = Minimizer()
        self.assertDictEqual({"PRIORITY": -1}, mini.plugin_config)
        self.assertListEqual([], mini.register_for)

        golden = {
            "PRIORITY": 2,
            "IMG_QUALITY": 70,
            "IMG_LONG_EDGE": 1920,
            "JS_OBFUSCATE": True,
            "JS_OBFUSCATE_GLOBALS": True,
            "CSS_INCLUDE_COMMENTS": False,
            "CSS_OUTPUT_STYLE": "compressed"
        }

        golden_register_for = ["png", "jpg", "jpeg", "tif", "tiff", "bmp", "js", "sass", "scss"]

        mini.config["MINIMIZER"] = {"PRIORITY": 2}
        mini.__init__()

        self.assertDictEqual(golden, mini.plugin_config)
        self.assertListEqual(golden_register_for, mini.register_for)

        # reset
        del mini.config["MINIMIZER"]
        mini.__init__()

    def test_register(self):
        mini = Minimizer()
        name, prio, ext = mini.register()

        self.assertEqual(name, "Minimizer")
        self.assertEqual(prio, -1)
        self.assertEqual(ext, [])

    @patch("barely.plugins.content.Minimizer.minimizer.Image")
    @patch("barely.plugins.content.Minimizer.minimizer.minify_print")
    @patch("barely.plugins.content.Minimizer.minimizer.es5")
    @patch("barely.plugins.content.Minimizer.minimizer.sass")
    def test_action(self, sass, es5, minifyjs, image):
        sass.compile = MagicMock(return_value="compiled")
        minifyjs.return_value = "smallerjs"
        image.thumbnail = MagicMock()

        item = {
            "destination": "",
            "output": "",
            "extension": "",
            "content_raw": ""
        }

        mini = Minimizer()
        mini.config["MINIMIZER"] = {"PRIORITY": 1}
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

        # Image
        item["image"] = image
        item["extension"] = "png"
        result = list(mini.action(item=item.copy()))[0]
        self.assertTrue(result["image"].thumbnail.called)
        self.assertEqual(result["quality"], 70)
        self.assertEqual(result["action"], "compressed")

        del mini.config["MINIMIZER"]
        mini.__init__()
