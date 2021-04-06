"""
auto-generate category pages from "collection"
meta-tags on the pages
"""
import os
from watchdog.events import FileModifiedEvent
from barely.plugins import PluginBase
from barely.core.EventHandler import EventHandler as EH
from barely.core.ProcessingPipeline import parse_meta, render_page, read_file, write_file


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
                "OVERVIEW_TEMPLATE": "",
                "COLLECTION_TEMPLATE": "",
                "SUMMARY_LENGTH": 100
            }
            self.plugin_config = standard_config | self.config["COLLECTIONS"]

            # need to get a full read on the current collections-situation.
            for root, dirs, files in os.walk(self.config["ROOT"]["DEV"], topdown=False):
                for path in files:
                    path = os.path.join(root, path)
                    if os.path.splitext(path)[1] == self.config["PAGE_EXT"]:
                        item = {
                            "origin": path
                        }
                        for it in parse_meta(read_file(item)):
                            self.action(item=it)
        except KeyError:
            self.plugin_config = {"PRIORITY": -1}

    def register(self):
        return "Collections", self.plugin_config["PRIORITY"], self.config["PAGE_EXT"]

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
                collectible["preview"] = item["content"][:self.plugin_config["SUMMARY_LENGTH"]] + "..."
                collectible["href"] = item["destination"].replace(self.plugin_config["ROOT"]["WEB"], "")
                collectible["timestamp"] = os.path.getmtime(item["origin"])

                # we'd also really like to get the first image of the blog

                # for integration with Timestamps
                if "last_edited" in item["meta"]:
                    collectible["date"] = item["meta"]["last_edited"]
                elif "created" in item["meta"]:
                    collectible["date"] = item["meta"]["created"]
                else:
                    collectible["date"] = "?"

                # for integration with ReadingTime
                if "title_image" in item["meta"]:
                    img_abspath = os.path.join(os.path.dirname(item["destination"]), item["meta"]["title_image"])
                    collectible["image"] = img_abspath

                # append the collectible to the appropriate ccllections
                # make sure there are no duplicatesthough! (determined by href)
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
                self.EXHIBITS.append(item["origin"])        # store for later (finalize re-renders these)
                wanted_exhibits = {}
                for exhibit in exhibits:
                    try:
                        wanted_exhibits[exhibit] = self.COLLECTION[exhibit]
                    except KeyError:
                        wanted_exhibits[exhibit] = []
                item["meta"]["exhibits"] = wanted_exhibits  # now contains all (current) exhibition-pieces from wanted collections
            except KeyError:
                pass

            yield item

    def finalize(self):
        for exhibitor in self.EXHIBITS:
            EH.notify(FileModifiedEvent(src_path=exhibitor))

        for col_name in self.COLLECTION:
            if self.plugin_config["COLLECTION_TEMPLATE"]:
                # every collection needs to be ordered (by mtime-stamp)
                collectibles = sorted(self.COLLECTION[col_name], key=lambda k: k["timestamp"], reverse=True)

                # the renderable collection page needs the following:
                # - a template: already got that during init, stored in config
                # - a destination: compound of PAGE and collection name
                # - metadata:   - a title
                #               - all the collectibles; they get referenced (or not!) in the template!
                # - content, content_raw: empty!
                # - action, origin: for logging
                page = {
                    "template": self.plugin_config["COLLECTION_TEMPLATE"],
                    "destination": os.path.join(self.config["ROOT"]["WEB"], self.plugin_config["PAGE"], col_name.lower(), "index.html"),
                    "meta": {
                        "title": col_name,
                        "collectibles": collectibles
                    },
                    "content": "",
                    "content_raw": "",
                    "action": "collected",
                    "origin": col_name
                }

                # mini pipeline, only the necessary steps
                write_file(render_page(parse_meta([page])))

        if self.plugin_config["OVERVIEW_TEMPLATE"]:
            # order collections by their size
            collections = []
            for c in self.COLLECTION:
                collections.append({
                    "name": c,
                    "size": len(self.COLLECTION[c]),
                    "href": os.path.join(self.config["ROOT"]["WEB"], self.plugin_config["PAGE"], c.lower(), "index.html")
                })
            collections = sorted(collections, key=lambda k: k["size"], reverse=True)

            page = {
                "template": self.plugin_config["OVERVIEW_TEMPLATE"],
                "destination": os.path.join(self.config["ROOT"]["WEB"], self.plugin_config["PAGE"], "index.html"),
                "meta": {
                    "title": self.plugin_config["OVERVIEW_TITLE"],
                    "collections": collections
                },
                "content": "",
                "content_raw": "",
                "action": "created overview",
                "origin": "all collections"
            }

            write_file(render_page(parse_meta([page])))
