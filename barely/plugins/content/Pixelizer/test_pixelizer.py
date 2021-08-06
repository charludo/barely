import unittest
from mock import patch
from unittest.mock import MagicMock
from barely.plugins.content.Pixelizer.pixelizer import Pixelizer


class TestPixelizer(unittest.TestCase):

    def test___init__(self):
        pix = Pixelizer()
        self.assertDictEqual({"PRIORITY": -1}, pix.plugin_config)
        self.assertListEqual([], pix.register_for)

        golden = {
            "PRIORITY": 2,
            "IMG_QUALITY": 70,
            "IMG_LONG_EDGE": 1920
        }

        golden_register_for = ["png", "jpg", "jpeg", "tif", "tiff", "bmp"]

        pix.config["PIXELIZER"] = {"PRIORITY": 2}
        pix.__init__()

        self.assertDictEqual(golden, pix.plugin_config)
        self.assertListEqual(golden_register_for, pix.register_for)

        # reset
        del pix.config["PIXELIZER"]
        pix.__init__()

    def test_register(self):
        pix = Pixelizer()
        name, prio, ext = pix.register()

        self.assertEqual(name, "Pixelizer")
        self.assertEqual(prio, -1)
        self.assertEqual(ext, [])

    @patch("barely.plugins.content.Pixelizer.pixelizer.Image")
    def test_action(self, image):
        image.thumbnail = MagicMock()

        item = {
            "destination": "",
            "output": "",
            "extension": "",
            "content_raw": ""
        }

        pix = Pixelizer()
        pix.config["PIXELIZER"] = {"PRIORITY": 1}
        pix.__init__()

        # Image
        item["image"] = image
        item["extension"] = "png"
        result = list(pix.action(item=item.copy()))[0]
        self.assertTrue(result["image"].thumbnail.called)
        self.assertEqual(result["quality"], 70)
        self.assertEqual(result["action"], "compressed")

        del pix.config["PIXELIZER"]
        pix.__init__()
