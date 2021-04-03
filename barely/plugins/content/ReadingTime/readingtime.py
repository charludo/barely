"""
estimate how long it will take to read a page
"""
from barely.plugins import PluginBase


class ReadingTime(PluginBase):
    # very rough estimate of the reading time in minutes

    def __init__(self):
        super().__init__()
        try:
            standard_config = {
                "PRIORITY": 850
            }
            self.plugin_config = standard_config | self.config["READING_TIME"]
        except KeyError:
            self.plugin_config = {"PRIORITY": 850}

    def register(self):
        return "ReadingTime", self.plugin_config["PRIORITY"], self.config["PAGE_EXT"]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]
            word_count = len(item["content"].split())
            slow = word_count // 90
            fast = word_count // 265
            item["meta"]["reading_time"] = fast + " - " + slow
            yield item
