"""
Pixelizer resizes, compresses, and
converts images into web-friendly
formats. It also transforms <img/>
tags in <picture> tags with fallback.
"""
from PIL import Image
from barely.plugins import PluginBase


class Pixelizer(PluginBase):
    # Minify provides functions to compile and reduce scss and js in size

    def __init__(self):
        super().__init__()
        try:
            standard_config = {
                "PRIORITY": 3,
                "TARGETS": [
                    "xl 1920 100",
                    "xs 400 40"
                ],
                "LAYOUTS": [
                    "(max-width: 1000px) 100vw",
                    "1000px"
                ]
            }
            self.plugin_config = standard_config | self.config["PIXELIZER"]
            self.func_map = {
                "png,jpg,jpeg,tif,tiff,bmp": self.minimize_image,
                self.config["PAGE_EXT"]: self.generate_tag
            }
            self.register_for = sum([group.split(",") for group in self.func_map.keys()], [])
        except KeyError:
            self.plugin_config = {"PRIORITY": -1}
            self.register_for = []

    def register(self):
        return "Pixelizer", self.plugin_config["PRIORITY"], self.register_for

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]
            for key, func in self.func_map.items():
                if item["extension"] in key:
                    yield func(item)

    def minimize_image(self, item):
        try:
            long_edge = int(self.plugin_config["IMG_LONG_EDGE"])
            size = long_edge, long_edge

            item["image"].thumbnail(size, Image.ANTIALIAS)
            item["quality"] = int(self.plugin_config["IMG_QUALITY"])
            item["action"] = "compressed"
        except Exception as e:
            self.logger.error(f"An Error occured while handling the image: {e}")
        return item

    def generate_tag(self, item):
        try:
            if "none" in item["meta"]["PIXELIZER"]:
                return item
        except KeyError:
            pass

        try:
            page_config = self.plugin_config | {
                "LAYOUTS": item["meta"]["PIXELIZER"]
            }
        except KeyError:
            page_config = self.plugin_config

        <picture>
            <source media="(max-width: 700px)" sizes="(max-width: 500px) 50vw, 10vw" srcset="stick-figure-narrow.png 138w, stick-figure-hd-narrow.png 138w">

            <source media="(max-width: 1400px)" sizes="(max-width: 1000px) 100vw, 50vw" srcset="stick-figure.png 416w, stick-figure-hd.png 416w">
            <img src="stick-original.png" alt="Human">
        </picture>
