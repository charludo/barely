"""
BackupManager. Requires from config:
- BACKUPS MAX

Provides methods to create backups
and to restore them.
"""

import os
import glob
from datetime import datetime
import shutil
from .config import config
from barely.common.decorators import Singleton


@Singleton
class BackupManager:
    """ provides methods for the creation and the restoration of backups """

    root_bak = ""
    root_dev = ""
    root_web = ""
    tag_web = "WEBROOT"
    tag_dev = "DEVROOT"

    max = 0

    def __init__(self):
        self.root_bak = config["ROOT"]["BAK"]
        self.root_dev = config["ROOT"]["DEV"]
        self.root_web = config["ROOT"]["WEB"]

        self.max = int(config["BACKUP"]["MAX"])

    def _do_backup(self, src, tag):
        backup_name = tag.upper() + "--" + datetime.now().strftime("%Y-%m-%d--%H-%M-%S-%f") + ".bak"
        shutil.copy(src, os.path.join(self.root_bak, backup_name), follow_symlinks=False)

        existing = sorted(glob.glob(os.path.join(self.root_bak + tag.upper()) + "--*"))
        while len(existing) > self.max:
            shutil.rmtree(existing.pop(-1))

    def _do_restore(self, file, dest):
        shutil.rmtree(dest)
        shutil.copytree(file, dest)

    def backup(self, web=True, dev=False):
        """ create a new backup. choose which parts of the project to backup """
        if web:
            self._do_backup(self.root_web, self.tag_web)
        if dev:
            self._do_backup(self.root_dev, self.tag_dev)

    def restore(self, web=True, dev=False, exact=""):
        """ restore a backup. no params passed will restore latest web backup. """
        if len(exact):
            exact = os.path.join(self.root_bak, exact)
            if self.tag_web in exact:
                dest = self.root_web
            elif self.tag_dev in exact:
                dest = self.root_dev
            else:
                raise FileNotFoundError("Backup file could not be found.")
            self._do_restore(exact, dest)
        else:
            if web:
                newest = max(glob.iglob(os.path.join(self.root_bak, self.tag_web) + "*", key=os.path.getctime))
                self._do_restore(newest, self.root_web)
            if dev:
                newest = max(glob.iglob(os.path.join(self.root_bak, self.tag_dev) + "*", key=os.path.getctime))
                self._do_restore(newest, self.root_dev)
