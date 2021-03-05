"""
Any actions concerning file translation
have to go through this class. It handles
move/delete events directly, and hands off
new/update events to the ProcessingPipeline
"""

from watchdog.events import FileCreatedEvent, FileModifiedEvent
from watchdog.events import FileDeletedEvent, DirDeletedEvent
from watchdog.events import FileMovedEvent, DirMovedEvent
from binaryornot.check import is_binary
from pathlib import Path
import shutil
import os
import re
from barely.common.config import config
from barely.common.utils import make_valid_path


class EventHandler():
    """ handle events, hand hem off, or diregard irrelevant ones """

    def __init__(self):
        pass

    def notify(self, event):
        """ anyone (but usually, the watchdog) can issue a notice of a file event """
        src_dev = event.src_path
        src_web = self._get_web_path(src_dev)

        if self.template_dir in src_dev and not isinstance(event, FileDeletedEvent) and not isinstance(event, DirDeletedEvent):
            for affected in self._get_affected(src_dev):
                self.notify(FileModifiedEvent(src_path=affected))
        elif "config.yaml" in src_dev or "metadata.yaml" in src_dev:
            # don't do anything. These changes don't have to be tracked.
            pass
        elif re.match(r"\/_\S+\/\S+.{config['PAGE_EXT']}", src_dev):
            parent_page = self._get_parent_page(src_dev)
            self.notify(FileModifiedEvent(src_path=parent_page))
        elif isinstance(event, FileDeletedEvent) or isinstance(event, DirDeletedEvent):
            self._delete(src_web)
        elif isinstance(event, FileMovedEvent) or isinstance(event, DirMovedEvent):
            dest_web = self._get_web_path(event.dest_path)
            self._move(src_web, dest_web)
        elif isinstance(event, FileCreatedEvent) or isinstance(event, FileModifiedEvent):
            type, extension = self._determine_type(src_dev)
            item = {
                "origin": src_dev,
                "destination": src_web,
                "type": type,
                "extension": extension
            }
            self.pipeline.process([item])
        else:
            pass

    def force_rebuild(self):
        """ rebuild the entire project by first deleting the devroot, then marking every file as new """
        self._delete(config["root"]["web"])
        os.makedirs(config["root"]["web"], exist_ok=True)
        for root, dirs, files in os.walk(config["ROOT"]["DEV"], topdown=False):
            for path in files:
                if self.template_dir not in path:
                    self.notify(FileCreatedEvent(src_path=os.path.join(root, path)))

    def _determine_type(self, path):
        """ determine the type of the file via its extension. return both """
        ext = os.path.splitext(path)[1]
        if ext == config["PAGE_EXT"]:
            return "PAGE", config["PAGE_EXT"]
        elif ext in config["IMAGE_EXT"]:
            return "IMAGE", ext
        elif not is_binary(path):
            return "TEXT", ext
        else:
            return "GENERIC", ext

    def _get_affected(self):
        """ yield the paths of all files that rely on a certain template """
        pass

    @staticmethod
    def _get_web_path(path):
        """ get where a file is supposed to go. depends on the type """
        path = path.replace(config["ROOT"]["DEV"], "")                     # remove devroot if exists
        path = path.replace(config["ROOT"]["WEB"], "")                     # remove webroot if exists
        path = make_valid_path(config["ROOT"]["WEB"], path)                # add web root in front, args in back

        # Seperate path into its three components: dirname; file name; file extension
        dirname = os.path.dirname(path)
        filename, extension = os.path.splitext(os.path.basename(path))

        if extension == config["PAGE_EXT"]:
            filename = "index"
            extension = ".html"

            web_path = make_valid_path(dirname, filename) + extension
            return web_path

    @staticmethod
    def _get_parent_page(sub_page):
        """ return the path of the parent of a subpage """
        parent_dir = os.path.dirname(os.path.dirname(sub_page))  # equals the dir of the parent
        parent_page = str(next(Path(parent_dir).rglob("*." + config["PAGE_EXT"])))
        return parent_page

    @staticmethod
    def _delete(path):
        """ delete a file or dir """
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

    @staticmethod
    def _move(fro, to):
        """ move a file or dir """
        os.makedirs(os.path.dirname(to), exist_ok=True)
        shutil.move(fro, to)
