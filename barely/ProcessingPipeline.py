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
        else:
            pipe_generic([item])


################################
#            PIPES             #
################################
def pipe_page(items):
    """ pipe together the filters for page files """
    write_file(render_page(hook_plugins(parse_page(read_file(items)))))


def pipe_image(items):
    """ pipe together the filters for image files """
    save_image(hook_plugins(load_image(items)))


def pipe_text(items):
    """ pipe together the filters for textbased, non-page files """
    write_file(hook_plugins(read_file(items)))


def pipe_generic(items):
    """ pipe together the filters for all other (generic) files """
    copy_file(hook_plugins(items))


def pipe_sub_page(item):
    """ pipe together the filters for sub pages. notably, they do not get written to a file """
    for rendered_subpage in render_page(hook_plugins(parse_page(read_file(item)))):
        yield rendered_subpage


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
        yield item


def write_file(items):
    """ filter that writes a text based file to its appropriate location """
    for item in items:
        try:
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
        item["image"].save()


def copy_file(items):
    """ filter that simply copies a file """
    for item in items:
        assert(os.path.exists(item["origin"]))

        path = os.path.dirname(item["destination"])
        if not os.path.exists(path):
            os.mkdir(path)
        shutil.copy(item["origin"], item["destination"])


################################
#        FILTERS (PAGES)       #
################################
def parse_page(items):
    """ filter that parses page files into dict values, including the page's content and its template """
    for item in items:
        # get the template path
        base = os.path.basename(item["origin"])
        subdirs = base.split(".")
        subdirs = subdirs[:-1]
        path = make_valid_path(*subdirs)
        item["template"] = path + ".html"

        # get the metadata.yaml
        try:
            with open(os.path.join(config["ROOT"]["DEV"], "metadata.yaml")) as file:
                meta_raw = file.read()
            meta = yaml.safe_load(meta_raw)
        except FileNotFoundError:
            meta = {}

        # extract the yaml from the template
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

        # extract the content from the yaml
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

        # if the page is modular; get the sub-pages
        try:
            sub_pages = item["meta"]["modular"]
        except KeyError:
            sub_pages = []

        for sub_page in sub_pages:
            # get the filepath
            sub_page_origin = str(next(Path(os.path.join(os.path.dirname(item["origin"]), sub_page).rglob("*.md"))))
            sub_page_item = {
                "origin": sub_page_origin,
                "type": "PAGE",
                "extension": "md"
            }
            for rendered_subpage in pipe_sub_page(sub_page_item):
                item["meta"]["sub_pages"].append(rendered_subpage)

        yield item


def render_page(items):
    """ filter that renders a dict and a jinja template into html """
    for item in items:
        page_template = jinja.get_template(item["template"])
        page_rendered = page_template.render(**item["meta"])
        yield page_rendered


################################
#       FILTERS (PLUGINS)      #
################################
def hook_plugins(items):
    """ filter that allows 3rd-party-plugins to go ham on content dicts """
    for item in items:
        yield item
