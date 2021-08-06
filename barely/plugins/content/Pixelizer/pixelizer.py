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
                "IMG_QUALITY": 70,
                "IMG_LONG_EDGE": 1920
            }
            self.plugin_config = standard_config | self.config["PIXELIZER"]
            self.func_map = {
                "png,jpg,jpeg,tif,tiff,bmp": self.minimize_image
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
