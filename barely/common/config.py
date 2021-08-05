"""
Load the config and return it as a dict
"""
import os
import yaml
import logging


class Config:
    """ just here to return the config """
    logger = logging.getLogger("base.core")
    config = {}

    def __init__(self):
        if os.environ.get("barely") is None:
            import sys
            self.logger.info("something went wrong; was barely started the proper way?")
            sys.exit()

        with open(os.path.join(os.path.dirname(__file__), "empty_config.yaml")) as file:
            empty_config = file.read()
        empty_dict = yaml.safe_load(empty_config)

        with open(os.path.join(os.environ.get("barely"), "config.yaml")) as file:
            raw_config = file.read()
        config_dict = yaml.safe_load(raw_config)

        config_dict = empty_dict | config_dict
        config_dict["PLUGIN_PATHS"] = self.get_plugin_locales()
        self.config = config_dict

    @staticmethod
    def get_plugin_locales():
        barely_dir = os.path.dirname(os.path.dirname(__file__))
        sysplugin_parent = os.path.join(barely_dir, "plugins")
        userplugin_parent = os.path.join(os.environ["barely_appdir"], "plugins")

        return {
            "SYS": {
                "CONTENT": os.path.join(sysplugin_parent, "content"),
                "BACKUP": os.path.join(sysplugin_parent, "backup"),
                "PUBLICATION": os.path.join(sysplugin_parent, "publication")
            },
            "USER": {
                "CONTENT": os.path.join(userplugin_parent, "content"),
                "BACKUP": os.path.join(userplugin_parent, "backup"),
                "PUBLICATION": os.path.join(userplugin_parent, "publication")
            }
        }

    def get_config(self):
        """ return the config """
        return self.config

    def set_config(self, new_config):
        """ override the config """
        self.config = new_config


config = Config().get_config()
