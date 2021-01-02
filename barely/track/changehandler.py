"""
The central component of barely.
This Singleton should be the only
actor ever making changes in the
web_root directory.

Call the provided functions to realize
any changes to the web_root.
"""
import os
from barely.common.utils import make_dir, delete, move, copy
from barely.common.config import config
from barely.render import RENDERER as R
from barely.common.decorators import Singleton


@Singleton
class ChangeHandler(object):
    """ ChangeHandler singleton realizes any and all file changes """

    def _update_file(self, dev, web):
        extension = os.path.splitext(dev)[1]

        if extension in config["FILETYPES"]["RENDERABLE"]:
            R.render(dev, web)
        elif extension in config["FILETYPES"]["COMPRESSABLE"]["JS"]:
            pass
        elif extension in config["FILETYPES"]["COMPRESSABLE"]["CSS"]:
            pass
        elif extension in config["FILETYPES"]["COMPRESSABLE"]["IMAGES"]:
            pass
        elif extension not in config["FILETYPES"]["IGNORE"]:
            copy(dev, web)

    def update_all(self, cleanup_needed=True):
        """ create backup, then force update everything """
        if cleanup_needed:
            # backup anlegen!!
            delete(config["ROOT"]["WEB"])
            make_dir(config["ROOT"]["WEB"])
        for root, dirs, files in os.walk(config["ROOT"]["DEV"], topdown=False):
            for path in dirs:
                self.notify_added_dir(os.path.join(root, path))
            for path in files:
                self.notify_added_file(os.path.join(root, path))

    @staticmethod
    def _announce(type, src, dest=""):
        additional = ""
        if dest:
            additional = f"to: {dest}"
        announcement = f"{type}: {src} {additional}"
        return announcement

    def notify_added_file(self, dev, web):
        """ notify the ChangeHandler of a new file """
        make_dir(web)
        self._update_file(dev, web)
        return self._announce("created", web)

    def notify_added_dir(self, web):
        """ notify the ChangeHandler of a new dir """
        make_dir(web)
        return self._announce("created", web)

    def notify_deleted(self, web):
        """ notify the ChangeHandler of the removal of a file or dir"""
        delete(web)
        return self._announce("deleted", web)

    def notify_moved_file(self, web_old, dev, web):
        """ notify the ChangeHandler of a moved file """
        delete(web_old)
        self._update_file(dev, web)
        return self._announce("moved", web_old, web)

    def notify_moved_dir(self, web_old, web):
        """ notify the ChangeHandler of a moved dir """
        move(web_old, web)
        return self._announce("moved", web_old, web)

    def notify_modified(self, dev, web):
        """ notify the ChangeHandler of a file modification """
        self._update_file(dev, web)
        return self._announce("updated", web)
