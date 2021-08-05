"""
Any actions concerning file translation
have to go through this class. It handles
move/delete events directly, and hands off
new/update events to the ProcessingPipeline
"""

from watchdog.events import FileCreatedEvent, FileModifiedEvent
from watchdog.events import FileDeletedEvent, DirDeletedEvent
from watchdog.events import FileMovedEvent, DirMovedEvent
from watchdog.events import DirModifiedEvent
from binaryornot.check import is_binary
from pathlib import Path
import os
import re
from barely.common.config import config
import barely.core.ProcessingPipeline as PP
import logging


class EventHandler():
    """ handle events, hand them off, or disregard irrelevant ones """
    logger = logging.getLogger("base.core")
    logger_indented = logging.getLogger("indented")

    @staticmethod
    def init_pipeline(PM):
        PP.init_jinja()
        PP.init_plugin_manager(PM)

    def notify(self, event):
        """ anyone (but usually, the watchdog) can issue a notice of a file event """

        if isinstance(event, DirModifiedEvent):
            self.logger.debug(f"ignored DirModifiedEvent at {event.src_path}")
            return

        src_dev = event.src_path
        src_web = self._get_web_path(src_dev)

        try:
            dest_dev = " -> " + event.dest_path
        except AttributeError:
            dest_dev = ""
        self.logger.info(f"event at {src_dev}{dest_dev}")

        if config["TEMPLATES_DIR"] in src_dev and not isinstance(event, FileDeletedEvent) and not isinstance(event, DirDeletedEvent):
            if isinstance(event, FileMovedEvent) or isinstance(event, DirMovedEvent):
                src_dev = event.dest_path

            self.logger_indented.info(f"event at {src_dev} affected pages:")
            for affected in self._get_affected(src_dev):
                self.notify(FileModifiedEvent(src_path=affected))
            self.logger_indented.info(f"done handling event at {src_dev}")
        elif "config.yaml" in src_dev or any(ignored in src_dev for ignored in config["IGNORE"]):
            # don't do anything. Config changes at runtime are not respected.
            self.logger.debug(f"event at ignored location {src_dev}")
            pass
        elif "metadata.yaml" in src_dev:
            self.logger.debug("metadata.yaml was changed!")
            self.notify(FileModifiedEvent(src_path=config["TEMPLATES_DIR"]))
        elif re.search(rf"[\\|\/]?_\S+[\\|\/]\S+\.{config['PAGE_EXT']}", src_dev):
            self.logger.debug(f"{src_dev} is a modular page")
            parent_page = self._get_parent_page(src_dev)
            self.notify(FileModifiedEvent(src_path=parent_page))
        elif isinstance(event, FileDeletedEvent) or isinstance(event, DirDeletedEvent):
            PP.delete(src_web)
        elif isinstance(event, FileMovedEvent) or isinstance(event, DirMovedEvent):
            dest_web = self._get_web_path(event.dest_path)
            if src_web == dest_web and isinstance(event, FileMovedEvent):
                self.notify(FileModifiedEvent(src_path=event.dest_path))
            else:
                PP.move(src_web, dest_web)
        elif isinstance(event, FileCreatedEvent) or isinstance(event, FileModifiedEvent):
            type, extension = self._determine_type(src_dev)
            self.logger.debug(f"determined {src_dev} is of type {type}")
            item = {
                "origin": src_dev,
                "destination": src_web,
                "type": type,
                "extension": extension
            }
            PP.process([item])

    def force_rebuild(self, start, light=False):
        """ rebuild parts of or the entire project """
        self.logger.info(f"rebuilding {start}...")

        # full rebuild, delete webroot
        if start == "devroot":
            self.logger.debug("rebuild is targeting the devroot")
            start = config["ROOT"]["DEV"]
            if not light:
                self.logger.debug("non-light rebuild will delete webroot")
                PP.delete(config["ROOT"]["WEB"])
                os.makedirs(config["ROOT"]["WEB"], exist_ok=True)
        elif not start.startswith(config["ROOT"]["DEV"]):
            self.logger.debug(f"converted {start} to abspath")
            start = os.path.join(config["ROOT"]["DEV"], start)

        # a file was specified; only rebuild it
        if os.path.isfile(start):
            self.logger.debug("rebuild is only targeting a single file")
            self.notify(FileCreatedEvent(src_path=start))
            return

        # rebuild all files in and below "start"
        for root, dirs, files in os.walk(start, topdown=False):
            for path in files:
                path = os.path.join(root, path)
                if (config["TEMPLATES_DIR"] not in path
                        and "config.yaml" not in path
                        and "metadata.yaml" not in path
                        and not any(ignored in path for ignored in config["IGNORE"])
                        and not re.search(rf"[\\|\/]?_\S+[\\|\/]\S+\.{config['PAGE_EXT']}", path)
                        and not (light and self._determine_type(path)[0] == "IMAGE")):     # light ignores images
                    self.notify(FileCreatedEvent(src_path=path))
        self.logger.info("rebuild complete.")

    def _get_affected(self, template):
        """ yield the paths of all files that rely on a certain template """
        self.logger.debug(f"finding all templates affected by change to {template}")

        # changes can occur on either files or dirs. If it's a dir, all files and subdirs are changed
        changed = []
        if type(template) == list:
            # since we don't know if the list contains dirs, files, or both,
            # this is easiest
            for t in template:
                yield from self._get_affected(t)
            return
        elif os.path.isfile(template):
            changed = [template]
        elif os.path.isdir(template):
            changed = [str(path) for path in Path(template).rglob("*.html")]

        # for every file that was directly changed, find all templates that
        # inherit from it, since these are also in need of a rerender
        affected = changed
        for parent in changed:
            affected.extend(self._find_children(parent))

        # extract the template name, such as it's used in the .md file names
        for element in range(len(affected)):
            affected[element] = affected[element].replace(config["ROOT"]["DEV"], "")
            affected[element] = affected[element].replace(config["TEMPLATES_DIR"], "")
            while affected[element][0] == os.sep:
                affected[element] = affected[element][1:]
            affected[element] = affected[element].replace(".html", "")
            affected[element] = affected[element].replace(os.sep, ".")
            affected[element] = os.sep + affected[element] + "." + config["PAGE_EXT"]
            self.logger.debug(f"identified {affected[element]} as affected by change to {template}")

        # find all renderable files
        file_candidates = []
        for path in Path(config["ROOT"]["DEV"]).rglob("*." + config["PAGE_EXT"]):
            file_candidates.append(str(path))

        # remove duplicate entries from the lists (prevents multiple re-renders)
        # mostly unnecessary, especially on the file_candidates, but just to be sure...
        affected = list(set(affected))
        file_candidates = list(set(file_candidates))
        # for every affected template, find all files that use this template.
        # then, re-render them.
        for template in affected:
            # the leading / is necessary to not match incomplete template paths/names
            for filename in file_candidates:
                if template in filename or template[1:] == filename:
                    yield filename

    def _find_children(self, parent):
        self.logger.debug(f"searching for children of {parent}")

        # find all templates. Yes, all of them.
        parent = parent.replace(os.path.join(config["ROOT"]["DEV"], ""), "")
        parent = parent.replace(os.path.join(config["TEMPLATES_DIR"], ""), "")
        parent = parent.replace(os.sep, "/")
        for path in Path(config["TEMPLATES_DIR"]).rglob("*.html"):
            # open them to check their contents
            with open(path, "r") as file:
                content = file.read()
                matches = re.findall(r'{%\s*(?:extends|include)\s+[\"|\']([^\"]+)[\"|\']\s*%}', content)
                # if an {% extends %} or {% include %} tag is found, this template is potentially affected!
                # check if it extends the one we're looking for.
                # return the children of the child (recursion!)
                # return the child
                if len(matches):
                    for match in matches:
                        if match == parent:
                            self.logger.debug(f"found a child: {str(path)}")
                            yield str(path)
                            yield from self._find_children(str(path))

    def _determine_type(self, path):
        """ determine the type of the file via its extension. return both """
        try:
            ext = os.path.splitext(path)[1][1:].lower()
        except IndexError:
            ext = ""
        try:
            if ext == config["PAGE_EXT"]:
                return "PAGE", config["PAGE_EXT"]
            elif ext in config["IMAGE_EXT"]:
                return "IMAGE", ext
            elif not is_binary(path) and ext != "":
                return "TEXT", ext
            elif is_binary(path):
                return "GENERIC", ext
            else:
                return "GENERIC", "NOTYPE"
        except FileNotFoundError:
            self.logger.debug(f"{path} vanished. Most likely a temp file.")

    @staticmethod
    def _get_web_path(path):
        """ get where a file is supposed to go. depends on the type """
        path = path.replace(config["ROOT"]["DEV"], "")                     # remove devroot if exists
        path = path.replace(config["ROOT"]["WEB"], "")                     # remove webroot if exists
        path = path[1:] if path[0] == os.sep else path                     # otherwise path is absolute, won't join
        path = os.path.join(config["ROOT"]["WEB"], path)                   # add web root in front, args in back
        # Seperate path into its three components: dirname; file name; file extension
        dirname = os.path.dirname(path)
        filename, extension = os.path.splitext(os.path.basename(path))

        if extension == "." + config["PAGE_EXT"]:
            filename = "index"
            extension = ".html"

        web_path = os.path.join(dirname, filename) + extension
        return web_path

    @staticmethod
    def _get_parent_page(sub_page):
        """ return the path of the parent of a subpage """
        parent_dir = os.path.dirname(os.path.dirname(sub_page))  # equals the dir of the parent
        try:
            parent_page = str(list(Path(parent_dir).glob("*." + config["PAGE_EXT"]))[0])
        except IndexError:
            raise IndexError("Child page has no parent!")
        return parent_page
