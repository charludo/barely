"""
The ProcessingPipeline is the heart of barely.py
The class provides various filters, and pipes them
together for four different cases:
    - pages
    - images
    - other text-based files
    - generic files
It also provides the hook for content plugins.
"""


class ProcessingPipeline():
    """ provides all the filters needed for barely to translate the templates and content into static websites """

    def __init__(self):
        pass

    def process(self):
        """ choose the applicable pipeline depending on the type """
        pass

    ################################
    #            PIPES             #
    ################################
    def _pipe_page(self):
        """ pipe together the filters for page files """
        pass

    def _pipe_image(self):
        """ pipe together the filters for image files """
        pass

    def _pipe_text(self):
        """ pipe together the filters for textbased, non-page files """
        pass

    def _pipe_generic(self):
        """ pipe together the filters for all other (generic) files """
        pass

    ################################
    #       FILTERS (FILEOPS)      #
    ################################
    def _read_file(self):
        """ filter that reads text based files """
        pass

    def _write_file(self):
        """ filter that writes a text based file to its appropriate location """
        pass

    def _load_image(self):
        """ filter that loads image files into PIL objects """
        pass

    def _save_image(self):
        """ filter that saves a PIL object into an image file """
        pass

    def _copy(self):
        """ filter that simply copies a file """
        pass

    ################################
    #        FILTERS (PAGES)       #
    ################################
    def _parse_page(self):
        """ filter that parses page files into dict values, including the page's content and its template """
        pass

    def _render_page(self):
        """ filter that renders a dict and a jinja template into html """
        pass

    ################################
    #       FILTERS (PLUGINS)      #
    ################################
    def _hook_plugins(self):
        """ filter that allows 3rd-party-plugins to go ham on content dicts """
        pass
