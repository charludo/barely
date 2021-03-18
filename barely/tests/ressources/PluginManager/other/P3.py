from barely.plugins import PluginBase


class PThree(PluginBase):
    def register(self):
        return "P3", 3
