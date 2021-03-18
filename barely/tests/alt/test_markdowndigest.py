import unittest
from barely.render import markdowndigest
from ref.utils import read, prepare_tempfiles, cleanup


class TestMarkdownDigest(unittest.TestCase):
    """ should be expanded to include more uncommon mk """
    maxDiff = None
    md = markdowndigest.MarkdownDigest()

    def test_get_html(self):

        prepare_tempfiles(yaml=0, markdown=1, out="html")
        self.assertEqual(self.md.get_html(read("in")), read("out"))
        cleanup()

        prepare_tempfiles(yaml=1, markdown=0, out="empty")
        self.assertEqual(self.md.get_html(read("in")), read("out"))
        cleanup()

        prepare_tempfiles(yaml=1, markdown=1, out="html")
        self.assertEqual(self.md.get_html(read("in")), read("out"))
        cleanup()

        prepare_tempfiles(yaml=2, markdown=1, out="yamlhtml")
        self.assertEqual(self.md.get_html(read("in")), read("out"))
        cleanup()

    def test_get_markdown(self):

        prepare_tempfiles(html=True, out="html")
        self.assertEqual(self.md.get_markdown(read("in"), False), read("out"))
        cleanup()

        prepare_tempfiles(html=True, out="htmlescaped")
        self.assertEqual(self.md.get_markdown(read("in"), True), read("out"))
        cleanup()
