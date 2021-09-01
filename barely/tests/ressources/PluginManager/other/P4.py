from barely.plugins import PluginBase


class PFour(PluginBase):
    def register(self):
        return "P4", 1

    def action(self, item):
        yield item
