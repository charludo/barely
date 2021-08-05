"""
The ProcessingPipeline is the heart of barely.py
It provides various filters, and pipes them
together for four different cases:
    - pages
    - images
    - other text-based files
    - generic files
It also provides the hook for content plugins.
"""

import re
import os
import yaml
import shutil
import mistune
import logging
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound, TemplateSyntaxError
from barely.common.config import config

logger = logging.getLogger("base.core")
logger_indented = logging.getLogger("indented")


def init_plugin_manager(PluginManager):
    global PM
    PM = PluginManager


def init_jinja():
    global jinja
    jinja = Environment(loader=FileSystemLoader(os.path.join(config["ROOT"]["DEV"], config["TEMPLATES_DIR"], "")))
    logger.debug("initialized jinja")


def log(item):
    logger_indented.info(f"{item['action']} {item['origin']} -> {item['destination']}")


def process(items):
    """ choose the applicable pipeline depending on the type """
    items = items if isinstance(items, list) else [items]
    minimum_dict = {
        "origin": "",
        "destination": "",
        "type": "",
        "extension": ""
    }

    for item in items:
        if not isinstance(item, dict):
            raise TypeError("Argument must be a dict")

        item = minimum_dict | item

        type = item["type"]
        if type == "PAGE":
            item["action"] = "rendered"
            pipe_page([item])
        elif type == "IMAGE":
            item["action"] = "saved"
            pipe_image([item])
        elif type == "TEXT":
            item["action"] = "saved"
            pipe_text([item])
        elif type == "GENERIC":
            item["action"] = "copied"
            pipe_generic([item])
        else:
            raise ValueError("Unknown FileType")


################################
#            PIPES             #
################################
def pipe_page(items):
    """ pipe together the filters for page files """
    write_file(render_page(hook_plugins(handle_subpages(parse_content(parse_meta(extract_template(read_file(items))))))))


def pipe_image(items):
    """ pipe together the filters for image files """
    save_image(hook_plugins(load_image(items)))


def pipe_text(items):
    """ pipe together the filters for textbased, non-page files """
    write_file(hook_plugins(read_file(items)))


def pipe_generic(items):
    """ pipe together the filters for all other (generic) files """
    copy_file(hook_plugins(items))


def pipe_subpage(item):
    """ pipe together the filters for subpages; only one level deep """
    for sub_page in render_page(hook_plugins(parse_content(parse_meta(extract_template(read_file(item)))))):
        yield sub_page


################################
#       FILTERS (FILEOPS)      #
################################
def read_file(items):
    """ filter that reads text based files """
    for item in items:
        logger.debug(f"reading file {item['origin']}")
        try:
            with open(item["origin"], 'r', encoding='utf-8') as file:
                raw_content = file.read()
                file.close()

            item["content_raw"] = raw_content
            item["output"] = raw_content        # default if no filter makes changes afterwards
            yield item
        except FileNotFoundError:
            raise FileNotFoundError("No file at specified origin.")


def write_file(items):
    """ filter that writes a text based file to its appropriate location """
    for item in items:
        # check for no_render flag
        try:
            if "no_render" in item["meta"] and item["meta"]["no_render"]:
                item["action"] = "did not render"
                continue
        except KeyError:
            pass
        # Change file extension if so configured
        try:
            path = os.path.splitext(item["destination"])[0]
            item["destination"] = path + "." + item["meta"]["extension"]
        except KeyError:
            pass

        logger.debug(f"writing file {item['destination']}")
        try:
            os.makedirs(os.path.dirname(item["destination"]), exist_ok=True)
            with open(item["destination"], 'w+', encoding='utf-8') as file:
                file.write(item["output"])
                file.close()
                log(item)
        except OSError as error:
            raise OSError(f"OSError: {error}")


def load_image(items):
    """ filter that loads image files into PIL objects """
    for item in items:
        logger.debug(f"loading image {item['origin']}")
        try:
            item["image"] = Image.open(item["origin"])
            yield item
        except FileNotFoundError:
            raise FileNotFoundError("No image at specified origin.")
        except UnidentifiedImageError:
            raise UnidentifiedImageError("Specified file is not an image.")


def save_image(items):
    """ filter that saves a PIL object into an image file """
    for item in items:
        logger.debug(f"saving image {item['origin']}")
        try:
            quality = item["quality"]
        except KeyError:
            quality = 100
        os.makedirs(os.path.dirname(item["destination"]), exist_ok=True)
        item["image"].save(item["destination"], optimize=True, quality=quality)
        log(item)


def copy_file(items):
    """ filter that simply copies a file """
    for item in items:
        try:
            os.makedirs(os.path.dirname(item["destination"]), exist_ok=True)
            shutil.copy(item["origin"], item["destination"])
            log(item)
        except FileNotFoundError:
            # most likely a temp file - disappeared during processing
            logger.debug(f"{item['origin']} vanished. Most likely a temp file.")


def delete(path):
    """ delete a file or dir """
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            logger_indented.info(f"deleted {path}")
    except FileNotFoundError:
        logger.debug(f"{path} vanished. Most likely a temp file.")


def move(fro, to):
    """ move a file or dir """
    try:
        if os.path.exists(to):
            if os.path.isfile(to):
                os.remove(to)
            else:
                shutil.rmtree(to)
        shutil.move(fro, to)
        logger_indented.info(f"moved {fro} -> {to}")
    except FileNotFoundError:
        raise FileNotFoundError("No file/dir at notification origin!")


################################
#        FILTERS (PAGES)       #
################################
def extract_template(items):
    """ filter that extracts the path of the template to be used in rendering """
    for item in items:
        base = os.path.basename(item["origin"])
        subdirs = base.split(".")
        subdirs = subdirs[:-1]
        path = os.path.join(*subdirs)
        item["template"] = path + ".html"
        logger.debug(f"{item['origin']} uses the template {item['template']}")

        yield item


def parse_meta(items):
    """ filter that gets the general and the page specific metadata (should they exist), and merges them """
    # get the general metadata
    try:
        with open(os.path.join(config["ROOT"]["DEV"], "metadata.yaml")) as file:
            meta_raw = file.read()
        meta = yaml.safe_load(meta_raw)
        meta = {} if meta is None else meta
    except FileNotFoundError:
        meta = {}

    # extract the page-specific yaml
    for item in items:
        # in case this is a sub page, the parent might have passed some meta to it
        try:
            parent_meta = item["parent_meta"]
        except KeyError:
            parent_meta = {}

        lines = item["content_raw"].splitlines(keepends=True)
        extracted_yaml = ""

        if not len(lines):
            page_meta = {}
        elif re.match(r"^---[\s|\t]*[\n|\r]?$", lines[0]):
            ln = 1
            while ln < len(lines) and not re.match(r"^---[\s|\t]*[\n|\r]?$", lines[ln]):
                extracted_yaml += lines[ln]
                ln += 1

            page_meta = yaml.safe_load(extracted_yaml)
        else:
            page_meta = {}

        item["meta"] = meta | parent_meta | page_meta

        yield item


def parse_content(items):
    """ filter that gets the actual content from a page """
    for item in items:
        lines = item["content_raw"].splitlines(keepends=True)

        ln = 0
        count = 0
        found = False
        while ln < len(lines) and not found:
            if re.match(r"^---[\s|\t]*[\n|\r]?$", lines[ln]):
                count += 1
            if count == 2:
                found = True
            ln += 1

        # yaml section found; only convert to html everything afterwards
        if found:
            item["content"] = mistune.html("".join(lines[ln::]))
        # no yaml section found; convert the entire document
        else:
            item["content"] = mistune.html(item["content_raw"])

        yield item


def handle_subpages(items):
    """ filter that finds and deals with subpages by means of a separate pipeline """
    for item in items:
        try:
            sub_pages = item["meta"]["modular"]
            item["meta"]["sub_pages"] = []
            logger.debug(f"{item['origin']} is modular! looking for subpages")
        except KeyError:
            sub_pages = []

        for sub_page in sub_pages:
            # get the filepath
            try:
                sub_page_origin = str(list(Path(os.path.join(os.path.dirname(item["origin"]), "_" + sub_page)).glob("*." + config["PAGE_EXT"]))[0])
                parent_meta = item["meta"].copy()
                parent_meta.pop("modular")
                parent_meta.pop("sub_pages")
                sub_page_item = {
                    "origin": sub_page_origin,
                    "type": "PAGE",
                    "extension": config["PAGE_EXT"],
                    "parent_meta": parent_meta
                }
                # only one level of subpages possible. this can easily be changed by including handle_subpages in this pipe.
                for rendered_subpage in pipe_subpage([sub_page_item]):
                    logger_indented.debug(f"rendered subpage {sub_page_item['origin']}")
                    item["meta"]["sub_pages"].append(rendered_subpage["output"])
            except FileNotFoundError:
                raise FileNotFoundError("Specified subpage does not exist.")
            except IndexError:    # Path found nothing
                raise IndexError("No subpages at specified location.")

        yield item


def render_page(items):
    """ filter that renders a dict and a jinja template into html """
    for item in items:
        try:
            page_template = jinja.get_template(item["template"])
            item["output"] = page_template.render(content=item["content"], **item["meta"])
            yield item
        except TemplateNotFound:
            logger.error(f"template \"{item['template']}\" not found")
        except TemplateSyntaxError as e:
            logger.error(f"template \"{item['template']}\" contains a Syntax Error: {e}")


################################
#       FILTERS (PLUGINS)      #
################################
def hook_plugins(items):
    """ filter that allows 3rd-party-plugins to go ham on item dicts """
    for item in items:
        for processed in PM.hook_content(item):
            yield processed
