from barely.plugins import PluginBase


class POne(PluginBase):
    def register(self):
        return "P1", 3, ["pdf", "png"]

    def action(self, item):
        yield item
