import os
import unittest
from src import renderer
from ref.utils import read, prepare_tempfiles, cleanup


class TestRenderer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.R = renderer.Renderer(template_path=os.path.join("test", "ref", "templates/"))

    def test_get_count(self):

        count = self.R.get_count()
        self.assertEqual(self.R.get_count(), count)

        prepare_tempfiles(yaml=1, markdown=1, out="template-rendered.html")
        self.R.render(os.path.join("test", "ref", "in"), os.path.join("test", "ref", "temp"))
        self.R.render(os.path.join("test", "ref", "in"), os.path.join("test", "ref", "temp"))
        cleanup()

        self.assertEqual(self.R.get_count(), count+2)

    def test_render(self):

        prepare_tempfiles(yaml=1, markdown=1, out="template-rendered.html")
        self.R.render(os.path.join("test", "ref", "in"), os.path.join("test", "ref", "temp"))
        self.assertEqual(read("temp"), read("out"))
        cleanup()

        prepare_tempfiles(yaml=0, markdown=1, out="template-rendered-noyaml.html")
        self.R.render(os.path.join("test", "ref", "in"), os.path.join("test", "ref", "temp"))
        self.assertEqual(read("temp"), read("out"))
        cleanup()

        prepare_tempfiles(yaml=1, markdown=0, out="template-rendered-nocontent.html")
        self.R.render(os.path.join("test", "ref", "in"), os.path.join("test", "ref", "temp"))
        self.assertEqual(read("temp"), read("out"))
        cleanup()
