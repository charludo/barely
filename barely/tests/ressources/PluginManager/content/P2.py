from barely.plugins import PluginBase


class PTwo(PluginBase):
    def register(self):
        return "P2", 1, ["md", "png"]

    def action(self, item):
        yield item
