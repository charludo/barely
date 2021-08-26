"""
Gallery converts a []!!() tag into a
list of globbed images from a specified dir
"""
import re
import os
import glob
from barely.plugins import PluginBase


class Gallery(PluginBase):
    # Turn a markdown tag into a gallery

    def __init__(self):
        super().__init__()
        standard_config = {
            "PRIORITY": 2,
            "DEFAULT_SORT": "name",
            "DEFAULT_DIRECTION": "asc",
            "GALLERY_CLASS": "gallery"
        }
        try:
            self.plugin_config = standard_config | self.config["GALLERY"]
        except KeyError:
            self.plugin_config = standard_config

    def register(self):
        return "Gallery", self.plugin_config["PRIORITY"], [self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]
            item["content"] = re.sub(r"\[(?P<name>\S+)\s?(?P<sort>\S+)?\s?(?P<direction>\S+)?\]!!\((?P<folder>\S+)\)", self._handle_matches, item["content"])
            yield item

    def _handle_matches(self, match):
        # get info from the gallery tag
        try:
            sort = match.group("sort")
        except KeyError:
            sort = self.plugin_config["DEFAULT_SORT"]

        try:
            direction = match.group("direction")
        except KeyError:
            direction = self.plugin_config["DEFAULT_DIRECTION"]

        name = match.group("name")
        folder = match.group("folder")
        path = folder

        self.logger.info(f"Generating gallery \"{name}\"...")

        if os.path.isabs(path):
            path = os.path.join(self.config["ROOT"]["DEV"], path.replace(self.config["ROOT"]["DEV"], "")[1:])
        else:
            path = os.path.join(self.config["ROOT"]["DEV"], path)

        # glob all images
        images = []
        types = [os.path.join(path, f"*.{t}") for t in self.config["IMAGE_EXT"]]
        for files in types:
            images.extend(glob.glob(files))

        # sort them
        if "time" in sort or "date" in sort:
            images = sorted(images, key=os.path.getmtime)
        else:
            images = sorted(images)

        # change direction if necessary
        if "desc" in direction:
            images.reverse()

        # build the gallery
        gallery = []
        gallery.append(f"<div class=\"{self.plugin_config['GALLERY_CLASS']}\" id=\"gallery-{name}\">")
        for image in images:
            image_path = image[image.index(folder):].replace('\\', '/')
            gallery.append(f"<img src=\"{image_path}\" alt=\"part of {name} gallery\">")
        gallery.append("</div>")

        return "\n".join(gallery)
