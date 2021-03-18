"""
During barelys startup, PluginManager
finds and registers all available
Plugins. This includes barelys core plugins,
as well as any the user might have put in their
dotfolder.
Plugins are being differntiated by their category
(content, backup or publication) and by the
filetype(s) they register for.
"""

from inspect import issubclass
from pkgutil import iter_modules
from importlib import import_module
from barely.common.config import config


class PluginBase:
    """ base class for all plugins """

    config = config

    def __init__(self, *args, **kwargs):
        pass

    def register(self):
        return "Base", -1, []

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            return kwargs.get("item")
        else:
            pass


class PluginManager:
    """ finds, registers and pipes in plugins """

    def __init__(self):
        self.plugins_content = self.discover_plugins([config["PLUGIN_PATHS"]["SYS"]["CONTENT"], [config["PLUGIN_PATHS"]["USER"]["CONTENT"]]])
        self.plugins_backup = self.discover_plugins([config["PLUGIN_PATHS"]["SYS"]["BACKUP"], [config["PLUGIN_PATHS"]["USER"]["BACKUP"]]], type_content=False)
        self.plugins_publication = self.discover_plugins([config["PLUGIN_PATHS"]["SYS"]["PUBLICATION"],
                                                         [config["PLUGIN_PATHS"]["USER"]["PUBLICATION"]]], type_content=False)

    def discover_plugins(self, paths, type_content=True):
        """ checks the path for plugin files, then imports them """
        found_plugins = {} if type_content else []
        for path in paths:
            for (_, module_name, _) in iter_modules([path]):

                module = import_module(f"{__name__}.{module_name}")
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)

                    if issubclass(attribute, PluginBase):
                        if type_content:
                            name, priority, registered_for = attribute.register()
                            for extension in registered_for:
                                found_plugins.setdefault(extension, []).append((attribute, priority))
                        else:
                            name, priority = attribute.register()
                            found_plugins.append((attribute, priority))

        if type_content:
            for ext, registered in found_plugins.items():
                registered.sort(key=lambda t: t[1])
                found_plugins[ext] = [r[0] for r in registered]
        else:
            found_plugins.sort(key=lambda t: t[1])
            found_plugins = [r[0] for r in found_plugins]

        return found_plugins

    def hook_content(self, item):
        item_list = [item]
        for plugin in self.plugins_content.get(item["extension"], default=[]):
            returned_items = []
            for i in item_list:
                for returned in plugin.action(item=i):
                    returned_items.append(returned)
            item_list = returned_items
        return item_list

    def hook_backup(self):
        for plugin in self.plugins_backup:
            plugin.action()

    def hook_publication(self):
        for plugin in self.plugins_publication:
            plugin.action()
