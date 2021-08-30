"""
Pixelizer resizes, compresses, and
converts images into web-friendly
formats. It also transforms <img/>
tags in <picture> tags with fallback.
"""
import re
import os
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
                    "lg 1000 70",
                    "md 650 70",
                    "sm 300 70"
                ],
                "LAYOUTS": [
                    "(max-width: 1000px) 100vw",
                    "1000px"
                ]
            }
            self.plugin_config = standard_config | self.config["PIXELIZER"]

            for i, t in enumerate(self.plugin_config["TARGETS"]):
                slug, width, quality = t.split()
                self.plugin_config["TARGETS"][i] = {
                    "slug": slug,
                    "width": int(width),
                    "quality": int(quality)
                }

            self.func_map = {
                "png,jpg,jpeg,tif,tiff,bmp": self.process_image,
                self.config["PAGE_EXT"]: self.process_page
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
                    yield from func(item)

    def process_image(self, item):
        item["action"] = "processed"
        filename = os.path.splitext(item["destination"])[0]

        for type in ["webp", item["extension"]]:
            for target in self.plugin_config["TARGETS"]:
                self.logger.debug(f"Started processing for type: {type}, target: {target['slug']}")
                variant = item.copy()
                variant["image"] = item["image"].copy()
                try:
                    _, original_y = item["image"].size
                    target_x = target["width"]
                    size = target_x, original_y
                    self.logger.debug(f"Original size: {item['image'].size}, New size: {size}")
                    variant["image"].thumbnail(size, Image.ANTIALIAS)
                    variant["quality"] = target["quality"]
                    variant["destination"] = f"{filename}-{target['slug']}.{type}"
                    variant["extension"] = type
                except Exception as e:
                    self.logger.error(f"An Error occured while handling the image: {e}")
                self.logger.debug(f"Finished processing for type: {type}, target: {target['slug']}")
                yield variant

        # copy the original as fallback
        item["copymode"] = True
        yield item

    def process_page(self, item):
        try:
            if "none" in item["meta"]["PIXELIZER"]:
                yield item
                return
        except KeyError:
            pass

        try:
            self.item_config = self.plugin_config.copy() | {
                "LAYOUTS": item["meta"]["PIXELIZER"]
            }
        except KeyError:
            self.item_config = self.plugin_config.copy()

        item["content"] = re.sub(r"<img(?:\s+alt=[\"'](?P<alt1>.*)[\"'])?\s+src=[\"'](?P<file>\S+)\.(?P<ext>[a-zA-Z]+)[\"'](?:\s+alt=[\"'](?P<alt2>.*)[\"'])?\s*[/]?>", self._generate_tag, item["content"])

        yield item

    def _generate_tag(self, match):
        file = match.group("file")
        ext = match.group("ext")
        alt = ""

        if match.group("alt2") is not None:
            alt = match.group("alt2")
        elif match.group("alt1") is not None:
            alt = match.group("alt1")

        if ext not in self.register_for:
            return f"<img src=\"{file}.{ext}\" alt=\"{alt}\">"

        sizes = ", ".join(self.item_config["LAYOUTS"])

        components = ["<picture>"]

        for type in ["webp", ext]:
            c = f"<source sizes=\"{sizes}\" srcset=\""

            srcset = []
            for target in self.item_config["TARGETS"]:
                srcset.append(f"{file}-{target['slug']}.{type} {target['width']}w")

            c += ", ".join(srcset)
            c += f"\" type=\"image/{type}\">"

            components.append(c)

        components.append(f"<img src=\"{file}.{ext}\" alt=\"{alt}\">")
        components.append("</picture>")

        return "\n".join(components)
