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
            "PRIORITY": 30,
            "KEYWORD_MODE": "append",
            "AUTO_KEYWORDS": True
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
            "keywords": "",
            "description": "",
            "site_name": "",
            "site_url": ""
        } | meta

    def register(self):
        return "AutoSEO", self.plugin_config["PRIORITY"], ["yaml", self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]

            try:
                page_seo = item["meta"]["SEO"]
            except KeyError:
                page_seo = {}

            def get_most_specific(tag):
                if tag in page_seo:
                    return page_seo[tag]
                elif tag in item["meta"]:
                    return item["meta"][tag]
                elif tag in self.meta:
                    return self.meta[tag]
                return None

            def get_global(tag):
                if tag in self.meta:
                    return {tag: self.meta[tag]}
                return {}

            # usw!! zusammen bauen mit: seo |= get_global(title) | get_page(title) | get_seo(title)

            # 1: page-specfic
            # 2: global meta
            # 3: generate / guess

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
