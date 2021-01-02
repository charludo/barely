import unittest
import os
from barely.common import utils
from barely.common.config import config


class TestUtils(unittest.TestCase):

    def test_read_file(self):
        test_string = """
            Das hier ist ein String.
            Das hier ist eine neue Zeile.

            Das hier ist ein neuer Absatz mit Sonderzeichen: äöüß€
        """

        with open("test.txt", "w") as file:
            file.write(test_string)
            file.close()

        self.assertEqual(utils.read_file("test.txt"), test_string)
        os.remove("test.txt")

    def test_get_template_path(self):
        self.assertEqual(utils.get_template_path("template"), "template.html")
        self.assertEqual(utils.get_template_path("template.subtemplate"), "template/subtemplate.html")
        self.assertEqual(utils.get_template_path("template.sub.template"), "template/sub/template.html")

    def test_make_valid_path(self):
        self.assertEqual(utils.make_valid_path("one", "two"), "one/two")
        self.assertEqual(utils.make_valid_path("one", "two.html"), "one/two.html")
        self.assertEqual(utils.make_valid_path("one", "two.jinja.html"), "one/two.jinja.html")
        self.assertEqual(utils.make_valid_path("/one", "two"), "/one/two")
        self.assertEqual(utils.make_valid_path("/one/", "two"), "/one/two")
        self.assertEqual(utils.make_valid_path("/one/", "two/"), "/one/two/")
        self.assertEqual(utils.make_valid_path("one", "/two/"), "/two/")

    def test_dev_to_web(self):
        devroot = config["ROOT"]["DEV"]
        webroot = config["ROOT"]["WEB"]

        self.assertEqual(utils.dev_to_web((devroot + "test.txt")), (webroot + "test.txt"))
        self.assertEqual(utils.dev_to_web((devroot + "test.sass")), (webroot + "test.css"))
        self.assertEqual(utils.dev_to_web((devroot + "test.js")), (webroot + "test.min.js"))
        self.assertEqual(utils.dev_to_web((devroot + "test.md")), (webroot + "index.html"))
