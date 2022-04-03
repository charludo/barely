"""
build a Table of Contents
from the heading, up to a
specified depth. insert IDs
into the <hx> tags to be able
to link to them
"""
import re
from barely.plugins import PluginBase


class ToC(PluginBase):
    # build a linked table of contents out of the html headings

    TOC = []

    def __init__(self):
        super().__init__()
        standard_config = {
            "PRIORITY": 2,
            "MIN_DEPTH": 1,
            "MAX_DEPTH": 4,
            "LIST_ELEMENT": "ul"
            }
        try:
            self.plugin_config = standard_config | self.config["TOC"]
        except KeyError:
            self.plugin_config = standard_config

    def register(self):
        return "ToC", self.plugin_config["PRIORITY"], [self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            self.TOC = []
            item = kwargs["item"]
            # should the generation be attempted a second time, the result will be an empty ToC!
            if "toc" not in item["meta"] and "parent_meta" not in item["meta"]:
                item["content"] = re.sub(r"<h(\d{1})>(.+)<\/h\d{1}>", self._handle_matches, item["content"])
                item["meta"]["toc"] = "\n".join(self._generate_toc())
            yield item

    def _handle_matches(self, match):
        level = match.group(1)
        heading = match.group(2)
        slug = re.sub(r"[^0-9a-zA-Z]+", "-", heading).lower()
        if int(level) >= self.plugin_config["MIN_DEPTH"] and int(level) <= self.plugin_config["MAX_DEPTH"]:
            self.TOC.append((int(level), heading, slug))
            return f'<h{level} id="{slug}">{heading}</h{level}>'
        else:
            return match.group(0)

    def _generate_toc(self):
        cur_lvl = self.plugin_config["MIN_DEPTH"] - 1

        yield '<div class="toc">'
        for index, (level, heading, slug) in enumerate(self.TOC):

            opened_layer = False
            while level > cur_lvl:
                if opened_layer:
                    yield "<li>"
                yield f"<{self.plugin_config['LIST_ELEMENT']}>"
                opened_layer = True
                cur_lvl += 1

            while level < cur_lvl:
                yield f"</{self.plugin_config['LIST_ELEMENT']}></li>"
                cur_lvl -= 1

            yield "<li>"
            yield f'<a href="#{slug}">{heading}</a>'
            if len(self.TOC) - 1 == index or self.TOC[index + 1][0] <= cur_lvl:
                yield "</li>"

        while self.plugin_config["MIN_DEPTH"] <= cur_lvl:
            yield f"</{self.plugin_config['LIST_ELEMENT']}>"
            if cur_lvl != self.plugin_config["MIN_DEPTH"]:
                yield "</li>"
            cur_lvl -= 1
        yield "</div>"
