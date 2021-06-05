"""
estimate how long it will take to read a page
"""
from barely.plugins import PluginBase


class ReadingTime(PluginBase):
    # very rough estimate of the reading time in minutes

    def __init__(self):
        super().__init__()
        standard_config = {
            "PRIORITY": 850,
            "WPM_FAST": 265,
            "WPM_SLOW": 90,
            "SEPARATOR": " - "
            }
        try:
            self.plugin_config = standard_config | self.config["READING_TIME"]
        except KeyError:
            self.plugin_config = standard_config

    def register(self):
        return "ReadingTime", self.plugin_config["PRIORITY"], [self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]
            word_count = len(item["content_raw"].split())
            slow = word_count // int(self.plugin_config["WPM_SLOW"])
            fast = word_count // int(self.plugin_config["WPM_FAST"])
            item["meta"]["reading_time"] = f"{fast}{self.plugin_config['SEPARATOR']}{slow}"
            yield item
