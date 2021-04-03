"""
BackupManager. Requires from config:
- BACKUPS MAX

Provides methods to create backups
and to restore them.
"""

import os
import glob
import shutil
from datetime import datetime
from barely.plugins import PluginBase


class LocalBackup(PluginBase):
    # save copies of the devroot in a local folder. very rudimentary backup strategy, but better than nothing, I guess.

    def __init__(self):
        super().__init__()
        try:
            standard_config = {
                "PRIORITY": 30,
                "MAX": 10,
                "BAKROOT": self.config["ROOT"]["BAK"]
            }
            if "LOCAL_BACKUP" in self.config:
                self.plugin_config = standard_config | self.config["TIMESTAMPS"]
            else:
                self.plugin_config = standard_config
        except KeyError:
            self.plugin_config = {"PRIORITY": -1}

    def register(self):
        return "LocalBackup", self.plugin_config["PRIORITY"]

    def action(self, *args, **kwargs):
        backup_name = "BACKUP--" + datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        shutil.copytree(self.config["ROOT"]["DEV"], os.path.join(self.plugin_config["BAKROOT"], backup_name), symlinks=False)

        existing = sorted(glob.glob(os.path.join(self.root_bak, "BACKUP--*"), reverse=True))
        while len(existing) > self.plugin_config["MAX"]:
            shutil.rmtree(existing.pop(-1))

        print(f"barely :: created backup: {backup_name}")
