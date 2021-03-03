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

import os
import shutil
from PIL import Image


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


################################
#       FILTERS (FILEOPS)      #
################################
def read_file(items):
    """ filter that reads text based files """
    for item in items:
        try:
            with open(item["origin"], 'r') as file:
                raw_content = file.read()
                file.close()
                yield raw_content
        except FileNotFoundError:
            raise FileNotFoundError("File '{0}' not found.".format(item["origin"]))
        except OSError as error:
            raise OSError("OS Error: {0}".format(error))


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
        item["image"] = Image.open(item["origin"])


def save_image(items):
    """ filter that saves a PIL object into an image file """
    for item in items:
        item["image"].save()


def copy_file(items):
    """ filter that simply copies a file """
    for item in items:
        path = os.path.dirname(item["destination"])
        if not os.path.exists(path):
            os.mkdir(path)
        shutil.copy(item["origin"], item["destination"])


################################
#        FILTERS (PAGES)       #
################################
def parse_page(items):
    """ filter that parses page files into dict values, including the page's content and its template """
    pass


def render_page(items):
    """ filter that renders a dict and a jinja template into html """
    pass


################################
#       FILTERS (PLUGINS)      #
################################
def hook_plugins(items):
    """ filter that allows 3rd-party-plugins to go ham on content dicts """
    pass
