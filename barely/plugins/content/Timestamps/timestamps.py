"""
timestamp pages with their creation date
and latest edit date, however do
respect user overrides
"""
from datetime import datetime
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
        return "Timestamps", self.plugin_config["PRIORITY"], self.config["PAGE_EXT"]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]
            if "last_edited" not in item["meta"]:                   # if last_edited set by user, we don't care
                now = datetime.now()                                # get current time to use as timestamp
                now = now.strftime(self.plugin_config["FORMAT"])    # format the time according to config

                if "created" in item["meta"]:                       # set creation date, wants latest edit date
                    item["meta"]["last_edited"] = now
                else:                                               # new file or doesn't care or wants always latest date
                    item["meta"]["created"] = now
            yield item
