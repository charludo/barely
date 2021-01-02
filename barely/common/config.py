"""
Load the config and return it as a dict
"""
import yaml
from .filereader import FileReader


class Config:
    """ just here to return the config """
    config = {}

    def __init__(self):
        fr = FileReader()
        raw_config = fr.get_raw("/home/charlotte/Webdesign/cms/barely/testing/config.yaml")
        config_dict = yaml.safe_load(raw_config)
        self.config = config_dict

    def get_config(self):
        """ return the config """
        return self.config

    def set_config(self, new_config):
        """ override the config """
        self.config = new_config


config = Config().get_config()
