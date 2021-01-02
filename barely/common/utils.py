"""
utility functions shared by
multiple classes
"""
import os
import shutil
from .config import config
from .replacements import replacements


def read_file(filename):
    from .filereader import FileReader
    fr = FileReader()
    return fr.get_raw(filename)


def get_template_path(template):
    """ helper function to get absolute path of the template to be used """
    dirs = template.split(".")
    dirs[-1] += ".html"
    return make_valid_path(*dirs)


def get_basename(path):
    return os.path.basename(path)


def make_valid_path(*args):
    return os.path.join(*args)


def dev_to_web(path):
    """ for a path in devroot, returns path in webroot (including changed extensions) """

    path = path.replace(config["ROOT"]["DEV"], "")                     # remove devroot if exists
    path = path.replace(config["ROOT"]["WEB"], "")                     # remove webroot if exists
    path = make_valid_path(config["ROOT"]["WEB"], path)                # add web root in front, args in back

    # Seperate path into its three components: dirname; file name; file extension
    dirname = os.path.dirname(path)
    filename = os.path.splitext(os.path.basename(path))[0]
    extension = os.path.splitext(os.path.basename(path))[1]

    if extension in config["FILETYPES"]["RENDERABLE"]:
        filename = replacements["renderable"]["name"]
        extension = replacements["renderable"]["extension"]
    elif extension in config["FILETYPES"]["COMPRESSABLE"]["JS"]:
        extension = replacements["compressable_js"]["extension"]
    elif extension in config["FILETYPES"]["COMPRESSABLE"]["CSS"]:
        extension = replacements["compressable_css"]["extension"]

    web_path = make_valid_path(dirname, filename) + extension
    return web_path


def make_dir(path):
    path = os.path.dirname(path)
    if not os.path.exists(path):
        os.mkdir(path)


def delete(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def move(old_path, new_path):
    shutil.move(old_path, new_path)


def copy(src, dest):
    shutil.copy(src, dest)
