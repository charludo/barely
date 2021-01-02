import unittest
from barely.render import yamldigest
from ref.utils import read, prepare_tempfiles, cleanup


class TestYAMLDigest(unittest.TestCase):

    yd = yamldigest.YAMLDigest()
    dict = eval(read("dict"))

    def test_get_dict(self):

        self.assertIsNone(self.yd.get_dict(read("empty")))
        self.assertIsNone(self.yd.get_dict(read("yamlnotontop")))

        prepare_tempfiles(yaml=1, markdown=0)
        self.assertDictEqual(self.yd.get_dict(read("in")), self.dict)
        cleanup()

        prepare_tempfiles(yaml=1, markdown=1)
        self.assertDictEqual(self.yd.get_dict(read("in")), self.dict)
        cleanup()

        prepare_tempfiles(yaml=2, markdown=0)
        self.assertDictEqual(self.yd.get_dict(read("in")), self.dict)
        cleanup()

        prepare_tempfiles(yaml=2, markdown=1)
        self.assertDictEqual(self.yd.get_dict(read("in")), self.dict)
        cleanup()

    def test_dump_yaml(self):

        prepare_tempfiles(dict=True, out="yaml")
        self.assertEqual(self.yd.dump_yaml(self.dict), read("yaml"))
