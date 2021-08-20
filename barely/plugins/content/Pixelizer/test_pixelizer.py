import re
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
            "TARGETS": [
                {
                    "slug": "lg",
                    "width": 1000,
                    "quality": 70
                },
                {
                    "slug": "md",
                    "width": 650,
                    "quality": 70
                },
                {
                    "slug": "sm",
                    "width": 300,
                    "quality": 70
                }
            ],
            "LAYOUTS": [
                "(max-width: 1000px) 100vw",
                "1000px"
            ]
        }

        golden_register_for = ["png", "jpg", "jpeg", "tif", "tiff", "bmp", "md"]

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
        # Testing the image handling
        image.thumbnail = MagicMock()
        image.size = 1920, 720

        item = {
            "destination": "/path/to/somewhere.png",
            "output": "",
            "extension": "png",
            "content_raw": "",
            "image": image
        }

        pix = Pixelizer()
        pix.config["PIXELIZER"] = {"PRIORITY": 1}
        pix.__init__()

        # Image
        result = list(pix.action(item=item.copy()))

        self.assertEqual(len(result), 7)

        self.assertEqual(result[0]["quality"], 100)
        self.assertEqual(result[0]["destination"], "/path/to/somewhere.png")
        self.assertEqual(result[0]["action"], "processed")

        self.assertEqual(result[1]["quality"], 70)
        self.assertEqual(result[1]["destination"], "/path/to/somewhere-lg.webp")
        self.assertEqual(result[1]["extension"], "webp")

        self.assertEqual(result[6]["quality"], 70)
        self.assertEqual(result[6]["destination"], "/path/to/somewhere-sm.png")
        self.assertEqual(result[6]["extension"], "png")

        # Testing the page handling

        item = {
            "extension": "md",
            "content": """
            <div class="test">
                <img alt="Test Image" src="some/source.jpg" />
            </div>
            """
        }

        golden = """
        <div class="test">
        <picture>
        <source sizes="(max-width: 1000px) 100vw, 1000px" srcset="some/source-lg.webp 1000w, some/source-md.webp 650w, some/source-sm.webp 300w" type="image/webp">
        <source sizes="(max-width: 1000px) 100vw, 1000px" srcset="some/source-lg.jpg 1000w, some/source-md.jpg 650w, some/source-sm.jpg 300w" type="image/jpg">
        <img src="some/source.jpg" alt="Test Image">
        </picture>
        </div>
        """
        result = list(pix.action(item=item.copy()))[0]

        self.assertEqual(re.sub(r'[\s+]', '', result["content"]), re.sub(r'[\s+]', '', golden))

        # "none"
        item = {
            "extension": "md",
            "content": """
            <div class="test">
                <img alt="Test Image" src="some/source.jpg" />
            </div>
            """,
            "meta": {
                "PIXELIZER": "none"
            }
        }
        result = list(pix.action(item=item.copy()))[0]
        self.assertDictEqual(result, item)

        # unsupported type
        item = {
            "extension": "md",
            "content": """
            <div class="test">
                <img alt="Test Image" src="some/source.gif" />
            </div>
            """
        }

        golden = {
            "extension": "md",
            "content": """
            <div class="test">
                <img src="some/source.gif" alt="Test Image">
            </div>
            """
        }
        result = list(pix.action(item=item.copy()))[0]
        self.assertDictEqual(result, golden)

        del pix.config["PIXELIZER"]
        pix.__init__()
