"""
Renders a yaml/markdown page and template
to a finished HTML Document and places it
at the appropriate place on the webserver

This is implemented as a singleton class.
"""

from jinja2 import Environment, FileSystemLoader
from .filereader import FileReader
from .utils import get_template_path, make_valid_path, get_basename
from .config import config


class Renderer(object):
    """ Renderer singleton provides a method to render a Page object to a HTML file """

    __instance = None

    _jinja_env = None
    _files_rendered = 0

    _fr = FileReader()

    def __new__(cls, template_path=""):
        if cls.__instance is None:
            cls.__instance == object.__new__(cls)
        return cls.__instance

    def __init__(self, template_path=""):
        if not len(template_path):
            template_root = make_valid_path(config["ROOT"]["DEV"], "templates/")
        else:
            template_root = template_path

        self._jinja_env = Environment(
            loader=FileSystemLoader(template_root)
            )

    def get_count(self):
        """ get the count of rendered pages. Utterly useless, but pylint won't leave me alone """
        return self._files_rendered

    def render(self, src, dest):
        """ Expects Source and Destination. Creates Page object to render to HTML and places it at dest """
        template = get_template_path(get_basename(src))
        content = self._fr.extract_markdown(src)
        params = self._fr.extract_yaml(src)

        page_template = self._jinja_env.get_template(template)
        page_rendered = page_template.render(content=content, context=params)

        try:
            with open(dest, 'w') as file:
                file.write(page_rendered)
                file.close()
            self._files_rendered += 1
            # print(f"Successfully rendered page to {dest}")
        except OSError as error:
            raise OSError(f"OSError: {error}")
