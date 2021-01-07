"""
The central component of barely.
This Singleton should be the only
actor ever making changes in the
web_root directory.

Call the provided functions to realize
any changes to the dev_root.
"""
import os
import re
from pathlib import Path
from barely.common.utils import make_dir, delete, move, copy, dev_to_web
from barely.common.config import config
from barely.render import RENDERER as R
from barely.common.decorators import Singleton


@Singleton
class ChangeHandler(object):
    """ ChangeHandler singleton realizes any and all file changes """

    def _update_file(self, dev, web):       # don't touch the damn /templates/ dir...
        templates_string = os.path.join(os.sep, "templates", "")
        if templates_string not in dev:
            extension = os.path.splitext(dev)[1]

            if extension in config["FILETYPES"]["RENDERABLE"]:
                R.render(dev, web)
            # elif extension in config["FILETYPES"]["COMPRESSABLE"]["JS"]:
                # pass
            # elif extension in config["FILETYPES"]["COMPRESSABLE"]["CSS"]:
                # pass
            # elif extension in config["FILETYPES"]["COMPRESSABLE"]["IMAGES"]:
                # pass
            elif extension not in config["FILETYPES"]["IGNORE"]:
                copy(dev, web)

    def update_all(self, backup=False):
        """ create backup, then force update everything """
        if backup:
            from barely.backup import BACKUPMANAGER as BAK
            BAK.backup(web=True, dev=False)
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

    def find_children(self, parent, template_dir):
        # find all templates. Yes, all of them.
        for path in Path(template_dir).rglob("*.html"):
            # open them to check their contents
            with open(path, "r") as file:
                content = file.read()
                matches = re.findall(r'{%\s*extends\s+[\"|\']([^\"]+)[\"|\']\s*%}', content)
                # if an {% extends %} tag is found, this template is affected!
                # check if it extends the one we're looking for.
                # return the children of the child (recursion!)
                # return the child
                if len(matches):
                    if os.path.join(template_dir, matches[0]) == parent:
                        yield from self.find_children(str(path), template_dir)
                        yield str(path)

    def notify_changed_template(self, template, template_dir, devroot=""):
        """ notify the ChangeHandler of changes to the templates """

        # used mostly for testing purposes
        if not len(devroot):
            devroot = config["ROOT"]["DEV"]

        # changes can occur on either files or dirs. If it's a dir, all files and subdirs are changed
        changed = []
        if os.path.isfile(template):
            changed = [template]
        elif os.path.isdir(template):
            changed = [str(path) for path in Path(template).rglob("*.html")]

        # for every file that was directly changed, find all templates that
        # inherit from it, since these are also in need of a rerender
        affected = changed
        for parent in changed:
            affected.extend(self.find_children(parent, template_dir))

        # extract the template name, such as it's used in the .md file names
        for element in range(len(affected)):
            template_dir = os.path.join(template_dir, "")
            affected[element] = affected[element].replace(template_dir, "")
            affected[element] = affected[element].replace(".html", "")
            affected[element] = affected[element].replace("/", ".")
            affected[element] = affected[element].replace("\\", ".")

        # find all renderable files. iterations depend on number of renderable file types
        file_candidates = []
        for ext in config["FILETYPES"]["RENDERABLE"]:
            for path in Path(devroot).rglob("*" + ext):
                file_candidates.append(str(path))

        # remove duplicate entries from the lists (prevents multiple re-renders)
        # mostly unnecessary, especially on the file_candidates, but just to be sure...
        affected = list(set(affected))
        file_candidates = list(set(file_candidates))

        # for every affected template, find all files that use this template.
        # then, re-render them.
        for template in affected:
            for filename in file_candidates:
                filename_ext = os.path.splitext(filename)
                this_template = os.path.join(os.sep, template) + filename_ext[1]
                if this_template in filename:
                    self._update_file(filename, dev_to_web(filename))
                    yield (template, filename)
