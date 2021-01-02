"""
Expects filename at instanciation.
Provides methods to return the YAML part of a file,
as well as the markdown part.

Throws FileNotFoundError if file not found.
Throws OSError if other problems during reading occurred.
"""
from .yamldigest import YAMLDigest
from .markdowndigest import MarkdownDigest


class FileReader:
    """ Reads a file, provides methods to return the yaml part and the markdown part. """
    _yd = YAMLDigest()
    _md = MarkdownDigest()

    def _read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                raw_content = file.read()
                file.close()
                return raw_content
        except FileNotFoundError:
            raise FileNotFoundError("File '{0}' not found.".format(filename))
        except OSError as error:
            raise OSError("OS Error: {0}".format(error))

    def extract_yaml(self, filename):
        """ Returns the YAML part of the file (everything between the two --- strings) """
        yaml = self._yd.get_dict(self._read_file(filename))
        return yaml

    def extract_markdown(self, filename):
        """ Returns the markdown part of the file (everything after the two --- strings) """
        markdown = self._md.get_html(self._read_file(filename))
        return markdown

    def get_raw(self, filename):
        """ return the entire file """
        return self._read_file(filename)
