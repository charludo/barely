import os
import unittest
from barely.render import RENDERER as R
from ref.utils import read, prepare_tempfiles, cleanup, testdir, infile, tempfile


class TestRenderer(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.R = R
        self.R.set_template_path(os.path.join(testdir, "templates/"))

    def test_get_count(self):

        count = self.R.get_count()
        self.assertEqual(self.R.get_count(), count)

        prepare_tempfiles(yaml=1, markdown=1, out="template-rendered.html")
        self.R.render(infile, tempfile)
        self.R.render(infile, tempfile)
        cleanup()

        self.assertEqual(self.R.get_count(), count+2)

    def test_render(self):

        prepare_tempfiles(yaml=1, markdown=1, out="template-rendered.html")
        self.R.render(infile, tempfile)
        self.assertEqual(read("temp"), read("out"))
        cleanup()

        prepare_tempfiles(yaml=0, markdown=1, out="template-rendered-noyaml.html")
        self.R.render(infile, tempfile)
        self.assertEqual(read("temp"), read("out"))
        cleanup()

        prepare_tempfiles(yaml=1, markdown=0, out="template-rendered-nocontent.html")
        self.R.render(infile, tempfile)
        self.assertEqual(read("temp"), read("out"))
        cleanup()
