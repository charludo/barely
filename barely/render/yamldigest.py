"""
Since this depends solely on pyyaml, having
a separate class is completely unnecessary.

The only reason it's here anyways is to help
with a uniform structure and the readability
of the module.
"""

import yaml
import re


class YAMLDigest:
    """ Converts a yaml string into a python object """

    def get_dict(self, yaml_raw):
        """ Expects a yaml string, returns a python dict """
        lines = yaml_raw.splitlines(keepends=True)
        extracted_yaml = ""

        if not len(lines):
            return None
        if re.match(r"^---[\s|\t]*[\n|\r]?$", lines[0]):
            ln = 1
            while ln < len(lines) and not re.match(r"^---[\s|\t]*[\n|\r]?$", lines[ln]):
                extracted_yaml += lines[ln]
                ln += 1

        yaml_dict = yaml.safe_load(extracted_yaml)
        return yaml_dict

    @staticmethod
    def dump_yaml(yaml_dict):
        """ Expects a python dict, returns a yaml string """
        yaml_raw = yaml.dump(yaml_dict)
        return yaml_raw
