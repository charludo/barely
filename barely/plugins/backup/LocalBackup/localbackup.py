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
                "BAKROOT": os.path.join(os.path.dirname(self.config["ROOT"]["DEV"]), "backups")
            }
            self.plugin_config = standard_config | self.config["LOCAL_BACKUP"]
        except KeyError:
            self.plugin_config = {"PRIORITY": -1}

    def register(self):
        return "LocalBackup", self.plugin_config["PRIORITY"]

    def action(self, *args, **kwargs):
        backup_name = "BACKUP--" + datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        backup_path = os.path.join(self.plugin_config["BAKROOT"], backup_name)
        shutil.copytree(self.config["ROOT"]["DEV"], backup_path, symlinks=False)

        existing = sorted(glob.glob(os.path.join(self.plugin_config["BAKROOT"], "BACKUP--*"), reverse=True))
        while len(existing) >= self.plugin_config["MAX"]:
            shutil.rmtree(existing.pop(-1))

        # we don't want to backup any existing git stuff
        try:
            shutil.rmtree(os.path.join(backup_path, ".git"))
        except FileNotFoundError:
            pass

        self.logger.info(f"created backup: {backup_name}")
