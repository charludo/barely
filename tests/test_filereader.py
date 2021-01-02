import unittest
import os
from src import filereader
from ref.utils import read, prepare_tempfiles, cleanup


class TestFileReader(unittest.TestCase):

    _fr = filereader.FileReader()
    dict = eval(read("dict"))

    def test_get_raw(self):

        self.assertRaises(FileNotFoundError, self._fr.get_raw, "fail.md")

        prepare_tempfiles(html=True, out="html")
        self.assertEqual(self._fr.get_raw(os.path.join("test", "ref", "in")), read("out"))
        cleanup()

        prepare_tempfiles(yaml=1, markdown=1, out="yamlmd")
        self.assertEqual(self._fr.get_raw(os.path.join("test", "ref", "in")), read("out"))
        cleanup()

    def test_extract_yaml(self):

        self.assertRaises(FileNotFoundError, self._fr.extract_yaml, "fail.md")

        prepare_tempfiles(yaml=1, markdown=1)
        self.assertDictEqual(self._fr.extract_yaml(os.path.join("test", "ref", "in")), self.dict)
        cleanup()

        prepare_tempfiles(yaml=1, markdown=0)
        self.assertDictEqual(self._fr.extract_yaml(os.path.join("test", "ref", "in")), self.dict)
        cleanup()

        prepare_tempfiles(yaml=0, markdown=1)
        self.assertEqual(self._fr.extract_yaml(os.path.join("test", "ref", "in")), None)
        cleanup()

    def test_extract_markdown(self):

        self.assertRaises(FileNotFoundError, self._fr.extract_markdown, "fail.md")

        prepare_tempfiles(yaml=1, markdown=1, out="html")
        self.assertEqual(self._fr.extract_markdown(os.path.join("test", "ref", "in")), read("out"))
        cleanup()

        prepare_tempfiles(yaml=1, markdown=0)
        self.assertEqual(self._fr.extract_markdown(os.path.join("test", "ref", "in")), "")
        cleanup()

        prepare_tempfiles(yaml=0, markdown=1, out="html")
        self.assertEqual(self._fr.extract_markdown(os.path.join("test", "ref", "in")), read("out"))
        cleanup()
