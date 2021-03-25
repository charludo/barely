"""
Minimizer exports the singleton Minimzer,
which in turn provides functons to minimize
images, javascript,...
It also functions as a sass/scss parser.
"""
import os
import sass
from PIL import Image
from calmjs.parse import es5
from calmjs.parse.unparsers.es5 import minify_print
from barely.plugins import PluginBase


class Minimizer(PluginBase):
    # Minimizer provides functions to reduce various formats in size

    def __init__(self):
        try:
            standard_config = {
                "PRIORITY": 3,
                "IMG_QUALITY": 70,
                "IMG_LONG_EDGE": 1920,
                "JS_OBFUSCATE": True,
                "JS_OBFUSCATE_GLOBALS": True,
                "CSS_OUTPUT_STYLE": "compressed"
            }
            self.plugin_config = standard_config | self.config["MINIMIZER"]
            self.func_map = {
                "png,jpg,jpeg,gif,tif,tiff,bmp": self.minimize_image,
                "js": self.minimize_js,
                "sass,scss,css": self.minimize_css
            }
            self.register_for = sum([group.split(",") for group in self.func_map.keys()], [])
        except KeyError:
            self.plugin_config = {"PRIORITY": -1}
            self.register_for = []

    def register(self):
        return "Minimizer", self.plugin_config["PRIORITY"], self.register_for

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]
            item["action"] = "compiled"
            item["destination"] = os.path.splitext(item["destination"])[0] + ".css"
            for key, func in self.func_map.items():
                if item["extension"] in key:
                    return func(item)

    def minimize_css(self, item):
        compiled = sass.compile_string(item["content_raw"], output_style=self.plugin_config["CSS_OUTPUT_STYLE"])
        item["content"] = compiled
        return item

    def minimize_js(self, item):
        minified = minify_print(es5(item["content_raw"]), obfuscate=self.plugin_config["JS_OBFUSCATE"],
                                obfuscate_globals=self.plugin_config["JS_OBFUSCATE_GLOBALS"])
        item["content"] = minified
        return item

    def minimize_image(self, item):
        long_edge = int(self.plugin_config["IMG_LONG_EDGE"])
        size = long_edge, long_edge

        item["image"].thumbnail(size, Image.ANTIALIAS)
        item["quality"] = self.plugin_config["IMG_QUALITY"]
        return item
