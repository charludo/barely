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
from PIL import Image
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from barely.common.config import config
from barely.common.utils import make_valid_path
from barely.plugins.PluginManager import PluginManager


PM = PluginManager()
jinja = Environment(loader=FileSystemLoader(make_valid_path(config["ROOT"]["DEV"], "templates", "")))


def process(items):
    """ choose the applicable pipeline depending on the type """
    for item in items:
        if item["type"] == "PAGE":
            pipe_page([item])
        elif item["type"] == "IMAGE":
            pipe_image([item])
        elif item["type"] == "TEXT":
            pipe_text([item])
        elif item["type"] == "GENERIC":
            pipe_generic([item])


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


################################
#       FILTERS (FILEOPS)      #
################################
def read_file(items):
    """ filter that reads text based files """
    for item in items:
        assert(os.path.exists(item["origin"]))

        with open(item["origin"], 'r') as file:
            raw_content = file.read()
            file.close()

        item["content_raw"] = raw_content
        item["output"] = raw_content        # default if no filter makes changes afterwards
        yield item


def write_file(items):
    """ filter that writes a text based file to its appropriate location """
    for item in items:
        try:
            os.makedirs(os.path.dirname(item["destination"]), exist_ok=True)
            with open(item["destination"], 'w') as file:
                file.write(item["output"])
                file.close()
        except OSError as error:
            raise OSError(f"OSError: {error}")


def load_image(items):
    """ filter that loads image files into PIL objects """
    for item in items:
        assert(os.path.exists(item["origin"]))
        item["image"] = Image.open(item["origin"])
        yield item


def save_image(items):
    """ filter that saves a PIL object into an image file """
    for item in items:
        os.makedirs(os.path.dirname(item["destination"]), exist_ok=True)
        item["image"].save(item["destination"])


def copy_file(items):
    """ filter that simply copies a file """
    for item in items:
        assert(os.path.exists(item["origin"]))

        os.makedirs(os.path.dirname(item["destination"]), exist_ok=True)
        shutil.copy(item["origin"], item["destination"])


################################
#        FILTERS (PAGES)       #
################################
def extract_template(items):
    """ filter that extracts the path of the template to be used in rendering """
    for item in items:
        base = os.path.basename(item["origin"])
        subdirs = base.split(".")
        subdirs = subdirs[:-1]
        path = make_valid_path(*subdirs)
        item["template"] = path + ".html"

        yield item


def parse_meta(items):
    """ filter that gets the general and the page specific metadata (should they exist), and merges them """
    # get the general metadata
    try:
        with open(os.path.join(config["ROOT"]["DEV"], "metadata.yaml")) as file:
            meta_raw = file.read()
        meta = yaml.safe_load(meta_raw)
    except FileNotFoundError:
        meta = {}

    # extract the page-specific yaml
    for item in items:
        lines = item["content_raw"].splitlines(keepends=True)
        extracted_yaml = ""

        if not len(lines):
            page_meta = {}
        if re.match(r"^---[\s|\t]*[\n|\r]?$", lines[0]):
            ln = 1
            while ln < len(lines) and not re.match(r"^---[\s|\t]*[\n|\r]?$", lines[ln]):
                extracted_yaml += lines[ln]
                ln += 1

            page_meta = yaml.safe_load(extracted_yaml)

        item["meta"] = meta | page_meta

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
        except KeyError:
            sub_pages = []

        for sub_page in sub_pages:
            # get the filepath
            sub_page_origin = str(next(Path(os.path.join(os.path.dirname(item["origin"]), sub_page)).rglob("*." + config["PAGE_EXT"])))
            sub_page_item = {
                "origin": sub_page_origin,
                "type": "PAGE",
                "extension": config["PAGE_EXT"]
            }
            # only one level of subpages possible. this can easily be changed by including handle_subpages in this pipe.
            for rendered_subpage in render_page(hook_plugins(parse_content(parse_meta(extract_template(read_file(sub_page_item)))))):
                item["meta"]["sub_pages"].append(rendered_subpage)

        yield item


def render_page(items):
    """ filter that renders a dict and a jinja template into html """
    for item in items:
        page_template = jinja.get_template(item["template"])
        item["output"] = page_template.render(**item["meta"])
        yield item


################################
#       FILTERS (PLUGINS)      #
################################
def hook_plugins(items):
    """ filter that allows 3rd-party-plugins to go ham on content dicts """
    for item in items:
        for processed in PM.hook_content(item):
            yield processed
