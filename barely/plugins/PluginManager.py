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
import logging
from inspect import isclass
from pkgutil import iter_modules
from importlib import import_module
from abc import ABC, abstractmethod
from collections.abc import Iterable
from barely.common.config import config


class PluginBase(ABC):
    """ base class for all plugins """

    def __init__(self, *args, **kwargs):
        self.config = config
        self.logger = logging.getLogger("base.plugin")
        self.logger_indented = logging.getLogger("indented")

    @abstractmethod
    def register(self):
        return "Base", -1, []

    @abstractmethod
    def action(self, item, *args, **kwargs):
        yield item

    def finalize(self):
        pass


class PluginManager:
    """ finds, registers and pipes in plugins """
    logger = logging.getLogger("base.core")

    plugin_count = 0

    def __init__(self):
        self.logger.info("registering plugins...")
        self.plugins_content = self.discover_plugins([config["PLUGIN_PATHS"]["SYS"]["CONTENT"], config["PLUGIN_PATHS"]["USER"]["CONTENT"]])
        self.plugins_backup = self.discover_plugins([config["PLUGIN_PATHS"]["SYS"]["BACKUP"], config["PLUGIN_PATHS"]["USER"]["BACKUP"]], type_content=False)
        self.plugins_publication = self.discover_plugins([config["PLUGIN_PATHS"]["SYS"]["PUBLICATION"],
                                                         config["PLUGIN_PATHS"]["USER"]["PUBLICATION"]], type_content=False)
        self.logger.info(f"{self.plugin_count} plugins registered.")

    def discover_plugins(self, paths, type_content=True):
        """ checks the path for plugin files, then imports them """

        module_paths = paths.copy()
        for path in paths:
            self.logger.debug(f"checking for plugins in {path}")
            if os.path.exists(path):
                subdirs = (next(os.walk(path))[1])                                  # get all first level subdirs
                module_paths.extend([os.path.join(path, sub) for sub in subdirs])   # necessary, otherwise wrong relative paths
        sys.path.extend(module_paths)                                               # necessary for python to import from here

        registered = []    # used to ensure no duplicate plugins will be registered

        found_plugins = {} if type_content else []
        for (_, module_name, _) in iter_modules(module_paths):
            try:
                module = import_module(f"{module_name}")
            except Exception:
                continue

            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)

                # necessary to filter out the imported parent class
                if isclass(attribute) and issubclass(attribute, PluginBase) and not issubclass(PluginBase, attribute):
                    # is that a long-ass try-except? yes. but if a plugin is broken, idk about knowing why, I just do not want to initialize it.

                    try:
                        plugin_instance = attribute()
                        if type_content:
                            name, priority, registered_for = plugin_instance.register()
                            if name in registered:
                                continue
                            registered.append(name)
                            self.logger.debug(f"found the content plugin {name} of priority {priority}")
                            priority = int(priority)
                            if priority > -1:
                                self.plugin_count += 1
                                for extension in registered_for:
                                    found_plugins.setdefault(extension, []).append((plugin_instance, priority))
                        else:
                            name, priority = plugin_instance.register()
                            if name in registered:
                                continue
                            registered.append(name)
                            self.logger.debug(f"found the plugin {name} of priority {priority}")
                            if priority > -1:
                                self.plugin_count += 1
                                found_plugins.append((plugin_instance, priority))
                    except Exception:
                        pass

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

    def finalize_content(self):
        plugins = set()
        for ext in self.plugins_content:
            for plugin in self.plugins_content[ext]:
                plugins.add(plugin)

        for plugin in plugins:
            name, _, _ = plugin.register()
            self.logger.info(f"Finalizing plugin {name}...")
            plugin.finalize()

    def hook_backup(self):
        for plugin in self.plugins_backup:
            plugin.action()

    def hook_publication(self):
        for plugin in self.plugins_publication:
            plugin.action()
