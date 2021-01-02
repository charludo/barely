"""
Since this depends solely on mistune, having
a separate class is completely unnecessary.

The only reason it's here anyways is to help
with a uniform structure and the readability
of the module.
"""

import mistune
import re


class MarkdownDigest:
    """ Converts markdown to HTML or vice versa """

    @staticmethod
    def get_html(markdown):
        """ Expects markdown, returns html """
        lines = markdown.splitlines(keepends=True)

        ln = 0
        count = 0
        found = False
        while ln < len(lines) and not found:
            if re.match(r"^---[\s|\t]*[\n|\r]?$", lines[ln]):
                count += 1
            if count == 2:
                return mistune.html("".join(lines[ln+1::]))
            ln += 1

        return mistune.html(markdown)

    def get_markdown(self, html, escape=False):
        """ Expects HTML, returns markdown """
        markdown = mistune.create_markdown(escape=escape)
        return markdown(html)
