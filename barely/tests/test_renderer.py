import os
import unittest
from barely.render import RENDERER as R
from ref.utils import read, prepare_tempfiles, cleanup, testdir, infile, tempfile, move


class TestRenderer(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.R = R
        self.R.set_template_path(os.path.join(testdir, "templates/"))

        self.infile = infile + ".md"

    def test_gather_media(self):
        media = self.R.gather_media(os.path.join(testdir, "gather_media"))

        self.assertIn("extensionless", media)
        self.assertIn("image.png", media)
        self.assertIn("extra.min.css", media)

        self.assertNotIn("sub", media)
        self.assertNotIn("renderable.md", media)
        self.assertNotIn("notincluded.jpg", media)
        self.assertNotIn("sub/notincluded.jpg", media)

        self.assertEqual(len(media), 3)

    def test_get_count(self):

        count = self.R.get_count()
        self.assertEqual(self.R.get_count(), count)

        prepare_tempfiles(yaml=1, markdown=1, out="template-rendered.html")
        move(infile, self.infile)
        self.R.render(self.infile, tempfile)
        self.R.render(self.infile, tempfile)
        move(self.infile, infile)
        cleanup()

        self.assertEqual(self.R.get_count(), count+2)

    def test_render(self):

        prepare_tempfiles(yaml=1, markdown=1, out="template-rendered.html")
        move(infile, self.infile)
        self.R.render(self.infile, tempfile)
        self.assertEqual(read("temp"), read("out"))
        move(self.infile, infile)
        cleanup()

        prepare_tempfiles(yaml=0, markdown=1, out="template-rendered-noyaml.html")
        move(infile, self.infile)
        self.R.render(self.infile, tempfile)
        self.assertEqual(read("temp"), read("out"))
        move(self.infile, infile)
        cleanup()

        prepare_tempfiles(yaml=1, markdown=0, out="template-rendered-nocontent.html")
        move(infile, self.infile)
        self.R.render(self.infile, tempfile)
        self.assertEqual(read("temp"), read("out"))
        move(self.infile, infile)
        cleanup()
