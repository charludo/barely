"""
auto-generate category pages from "collection"
meta-tags on the pages
"""

import glob
from os import sep, walk
from os.path import dirname, getmtime, join, splitext

import yaml
from watchdog.events import FileModifiedEvent

from barely.core.EventHandler import EventHandler as EH
from barely.core.ProcessingPipeline import (
    hook_plugins,
    parse_content,
    parse_meta,
    read_file,
    render_page,
    write_file,
)
from barely.plugins import PluginBase
from barely.plugins.PluginManager import PluginManager as PM


class Collections(PluginBase):
    # Collections allow for categorizing pages, like you'd find in a blog

    COLLECTION = {}
    EXHIBITS = set()

    def __init__(self):
        super().__init__()
        try:
            standard_config = {
                "PRIORITY": 999,
                "PAGE": "categories",
                "OVERVIEW_TITLE": "",
                "OVERVIEW_CONTENT": "",
                "OVERVIEW_TEMPLATE": "",
                "COLLECTION_TEMPLATE": "",
                "SUMMARY_LENGTH": 100,
                "ORDER_KEY": "timestamp",
                "ORDER_REVERSE": True,
            }
            self.plugin_config = standard_config | self.config["COLLECTIONS"]

            # need to get a full read on the current collections-situation.
            for file in glob.iglob(
                join(self.config["ROOT"]["DEV"], "**", "*.md"), recursive=True
            ):
                item = {"origin": file, "destination": EH._get_web_path(file)}
                for it in parse_content(parse_meta(read_file([item]))):
                    _ = list(self.action(item=it))

        except KeyError:
            self.plugin_config = {"PRIORITY": -1}

    def register(self):
        return "Collections", self.plugin_config["PRIORITY"], [self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        # PAGE can be part of COLLECTIONS
        if "item" in kwargs:
            item = kwargs["item"]
            try:
                collections = item["meta"]["collections"]

                # extract necessary info from page:
                # - title of the page
                # - content, up to a certain cutoff
                # - the href of the rendered page

                collectible = {}
                collectible["title"] = item["meta"]["title"]
                collectible["origin"] = item["origin"]
                collectible["destination"] = item["destination"]
                collectible["extension"] = self.config["PAGE_EXT"]
                collectible["raw"] = item["content_raw"]
                collectible["href"] = (
                    item["destination"]
                    .replace(self.config["ROOT"]["WEB"], "", 1)
                    .replace("\\", "/")
                )
                collectible["meta"] = item["meta"]
                try:
                    collectible["timestamp"] = getmtime(item["origin"])
                except FileNotFoundError:
                    collectible["timestamp"] = "?"

                # is there an existing summary? probably a better preview
                try:
                    collectible["preview"] = item["meta"]["summary"]
                except KeyError:
                    collectible["preview"] = (
                        item["content"][: self.plugin_config["SUMMARY_LENGTH"]] + "..."
                    )

                # we'd also really like to get the first image of the blog
                if "title_image" in item["meta"]:
                    collectible["image"] = item["meta"]["title_image"]

                # for integration with Timestamps
                if "edited" in item["meta"]:
                    collectible["date"] = item["meta"]["edited"]
                if "created" in item["meta"]:
                    collectible["date"] = item["meta"]["created"]
                else:
                    collectible["date"] = ""

                # for integration with ReadingTime
                try:
                    collectible["reading_time"] = item["meta"]["reading_time"]
                except KeyError:
                    pass
                # append the collectible to the appropriate ccllections
                # make sure there are no duplicates though! (determined by href)
                for c in collections:
                    self.COLLECTION.setdefault(c, [])

                    i = 0
                    while i < len(self.COLLECTION[c]):
                        older = self.COLLECTION[c][i]
                        if collectible["href"] == older["href"]:
                            self.COLLECTION[c].pop(i)
                        i += 1
                    self.COLLECTION[c].append(collectible)
            except KeyError:
                pass

            # PAGE can want to display EXHIBITS
            try:
                exhibits = item["meta"]["exhibits"]
                self.EXHIBITS.add(
                    item["origin"]
                )  # store for later (finalize re-renders these)
                wanted_exhibits = {}
                for exhibit in exhibits:
                    try:
                        wanted_exhibits[exhibit] = sorted(
                            self.COLLECTION[exhibit],
                            key=self.sort_fn,
                            reverse=self.plugin_config["ORDER_REVERSE"],
                        )
                    except KeyError:
                        wanted_exhibits[exhibit] = []
                item["meta"]["exhibits"] = (
                    wanted_exhibits  # now contains all (current) exhibition-pieces from wanted collections
                )
            except KeyError:
                pass

            yield item

    def finalize(self):
        pm = PM()
        eh = EH()
        eh.init_pipeline(pm)

        for collection in self.COLLECTION:
            for item in self.COLLECTION[collection]:
                for it in hook_plugins(parse_content(parse_meta(read_file([item])))):
                    _ = list(self.action(item=it))

        frozen_exhibits = self.EXHIBITS
        for exhibitor in frozen_exhibits:
            eh.notify(FileModifiedEvent(src_path=exhibitor))

        if self.plugin_config["COLLECTION_TEMPLATE"]:
            for col_name in self.COLLECTION:
                # every collection needs to be ordered (by mtime-stamp)
                collectibles = sorted(
                    self.COLLECTION[col_name],
                    key=self.sort_fn,
                    reverse=self.plugin_config["ORDER_REVERSE"],
                )

                # the renderable collection page needs the following:
                # - a template: already got that during init, stored in config
                # - a destination: compound of PAGE and collection name
                # - metadata:   - a title
                #               - all the collectibles; they get referenced (or not!) in the template!
                # - content, content_raw: empty!
                # - action, origin: for logging
                page = {
                    "template": self.plugin_config["COLLECTION_TEMPLATE"],
                    "destination": join(
                        self.config["ROOT"]["WEB"],
                        self.plugin_config["PAGE"],
                        col_name.lower(),
                        "index.html",
                    ),
                    "meta": {"title": col_name, "collectibles": collectibles},
                    "content": "",
                    "content_raw": "",
                    "action": "collected",
                    "origin": col_name,
                    "extension": self.config["PAGE_EXT"],
                }

                # mini pipeline, only the necessary steps
                write_file(render_page(hook_plugins(parse_meta([page]))))

        if self.plugin_config["OVERVIEW_TEMPLATE"]:
            # order collections by their size
            collections = []
            for c in self.COLLECTION:
                collections.append(
                    {
                        "name": c,
                        "size": len(self.COLLECTION[c]),
                        "href": join(
                            sep, self.plugin_config["PAGE"], c.lower(), "index.html"
                        ).replace("\\", "/"),
                    }
                )
            collections = sorted(collections, key=lambda k: k["size"], reverse=True)

            if self.plugin_config["OVERVIEW_CONTENT"]:
                origin = join(
                    self.config["ROOT"]["DEV"],
                    self.plugin_config["OVERVIEW_CONTENT"].lstrip("/\\"),
                )
                processed = list(parse_content(read_file([{"origin": origin}])))[0]
                content = processed["content"]
                content_raw = processed["content_raw"]
            else:
                origin = "all collections"
                content = ""
                content_raw = ""

            page = {
                "template": self.plugin_config["OVERVIEW_TEMPLATE"],
                "destination": join(
                    self.config["ROOT"]["WEB"], self.plugin_config["PAGE"], "index.html"
                ),
                "meta": {
                    "title": self.plugin_config["OVERVIEW_TITLE"],
                    "collections_list": collections,
                },
                "content": content,
                "content_raw": content_raw,
                "action": "created overview",
                "origin": origin,
                "extension": self.config["PAGE_EXT"],
            }

            write_file(render_page(hook_plugins(parse_meta([page]))))

    def sort_fn(self, item):
        key = self.plugin_config["ORDER_KEY"]
        if value := item.get(key, None):
            return value
        return item["meta"].get(key, None)
