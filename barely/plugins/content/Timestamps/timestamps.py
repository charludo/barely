"""
timestamp pages with their creation date
and latest edit date, however do
respect user overrides
"""
from datetime import datetime
from os.path import getctime, getmtime
from barely.plugins import PluginBase


class Timestamps(PluginBase):
    # Timestamps guesses what the user is interested in and sets timestamps accordingly

    def __init__(self):
        super().__init__()
        try:
            standard_config = {
                "PRIORITY": 3,
                "FORMAT": "%d.%m.%Y"
            }
            self.plugin_config = standard_config | self.config["TIMESTAMPS"]
        except KeyError:
            self.plugin_config = {"PRIORITY": -1}

    def register(self):
        return "Timestamps", self.plugin_config["PRIORITY"], [self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]

            ctime = datetime.fromtimestamp(getctime(item["origin"])).strftime(self.plugin_config["FORMAT"])
            mtime = datetime.fromtimestamp(getmtime(item["origin"])).strftime(self.plugin_config["FORMAT"])

            if "created" not in item["meta"]:              # if not set by user, set Created Time
                item["meta"]["created"] = ctime
            if "edited" not in item["meta"]:               # if not set by user, set Modified Time
                item["meta"]["edited"] = mtime

            yield item
