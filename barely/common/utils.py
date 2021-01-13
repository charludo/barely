"""
utility functions shared by
multiple classes
"""
import os
import sys
import shutil
from contextlib import contextmanager
from .config import config
from .replacements import replacements


def read_file(filename):
    try:
        with open(filename, 'r') as file:
            raw_content = file.read()
            file.close()
            return raw_content
    except FileNotFoundError:
        raise FileNotFoundError("File '{0}' not found.".format(filename))
    except OSError as error:
        raise OSError("OS Error: {0}".format(error))


def write_file(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
            file.close()
    except OSError as error:
        raise OSError(f"OSError: {error}")


def get_template_path(template):
    """ helper function to get absolute path of the template to be used """
    base = os.path.basename(template)
    subdirs = base.split(".")
    subdirs = subdirs[:-1]
    path = make_valid_path(*subdirs)
    return path + ".html"


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


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def get_extension(path):
    name, ext = os.path.splitext(os.path.basename(path))
    return ext
