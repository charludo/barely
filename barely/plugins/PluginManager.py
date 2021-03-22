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

import os
import sys
from inspect import isclass
from pkgutil import iter_modules
from importlib import import_module
from collections.abc import Iterable
from barely.common.config import config


class PluginBase:
    """ base class for all plugins """

    def __init__(self, *args, **kwargs):
        self.config = config

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
        module_paths = paths.copy()
        for path in paths:
            if os.path.exists(path):
                subdirs = (next(os.walk(path))[1])                                  # get all first level subdirs
                module_paths.extend([os.path.join(path, sub) for sub in subdirs])   # necessary, otherwise wrong relative paths
        sys.path.extend(module_paths)                                           # necessary for python to import from here

        found_plugins = {} if type_content else []
        for (_, module_name, _) in iter_modules(module_paths):
            module = import_module(f"{module_name}")

            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)

                # necessary to filter out the imported parent class
                if isclass(attribute) and issubclass(attribute, PluginBase) and not issubclass(PluginBase, attribute):
                    if type_content:
                        name, priority, registered_for = attribute().register()
                        if priority > -1:
                            for extension in registered_for:
                                found_plugins.setdefault(extension, []).append((attribute, priority))
                    else:
                        name, priority = attribute().register()
                        if priority > -1:
                            found_plugins.append((attribute, priority))

        sys.path = list(set(sys.path) - set(module_paths))                      # remove our added entries to path

        if type_content:
            for ext, registered in found_plugins.items():
                registered.sort(key=lambda t: t[1])
                found_plugins[ext] = [r[0] for r in registered]
        else:
            found_plugins.sort(key=lambda t: t[1])
            found_plugins = [r[0] for r in found_plugins]

        return found_plugins

    def hook_content(self, to_hook):
        item_list = [to_hook]
        for plugin in self.plugins_content.get(to_hook["extension"], []):
            returned_items = []
            for i in item_list:
                returned = plugin.action(item=i)
                if isinstance(returned, Iterable) and not isinstance(returned, str):
                    for r in returned:
                        returned_items.append(r)
                else:
                    returned_items.append(returned)
            item_list = returned_items
        return item_list

    def hook_backup(self):
        for plugin in self.plugins_backup:
            plugin.action()

    def hook_publication(self):
        for plugin in self.plugins_publication:
            plugin.action()
