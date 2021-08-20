"""
auto-generate lots of SEO-relevant tags

...because doing it manually is boring.
"""
import os
import yaml
from barely.plugins import PluginBase


class AutoSEO(PluginBase):

    def __init__(self):
        super().__init__()
        standard_config = {
            "PRIORITY": 30
        }
        try:
            self.plugin_config = standard_config | self.config["AUTO_SEO"]
        except KeyError:
            self.plugin_config = standard_config

        try:
            with open(os.path.join(self.config["ROOT"]["DEV"], "metadata.yaml")) as file:
                meta_raw = file.read()
            meta = yaml.safe_load(meta_raw)
            meta = {} if meta is None else meta
        except FileNotFoundError:
            meta = {}

        self.meta = {
            "title": "",
            "description": "",
            "site_name": "",
            "site_url": ""
        } | meta

    def register(self):
        return "AutoSEO", self.plugin_config["PRIORITY"], ["yaml", self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]

            # title
            # description
            # robots

            # og:title
            # og:description
            # og:image
            # og:url
            # og:site_name

            # twitter:image:alt
            # twitter:card

            yield item

    def finalize(self):
        # robots.txt
        # sitemap
        pass
