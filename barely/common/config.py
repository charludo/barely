"""
Load the config and return it as a dict
"""
import yaml
from .decorators import Singleton


@Singleton
class Config:
    """ just here to return the config """
    config = {}

    def __init__(self):
        with open("/home/charlotte/Webdesign/barely/blueprints/config.yaml") as file:
            raw_config = file.read()
        config_dict = yaml.safe_load(raw_config)
        self.config = config_dict

    def get_config(self):
        """ return the config """
        return self.config

    def set_config(self, new_config):
        """ override the config """
        self.config = new_config


config = Config.instance().get_config()
