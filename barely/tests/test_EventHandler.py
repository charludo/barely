import os
import unittest
from mock import patch
from barely.common.config import config
from barely.core.EventHandler import EventHandler


class TestEventHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.chdir("EventHandler")
        self.EH = EventHandler()

    @classmethod
    def tearDownClass(self):
        os.chdir("..")

    def test_notify(self):
        pass

    def test_force_rebuild(self):
        pass

    def test__determine_type(self):
        os.chdir("type")
        self.assertTupleEqual(("PAGE", "md"), self.EH._determine_type("file.md"))
        self.assertTupleEqual(("IMAGE", "png"), self.EH._determine_type("file.png"))
        self.assertTupleEqual(("TEXT", "css"), self.EH._determine_type("file.css"))
        self.assertTupleEqual(("GENERIC", "mp4"), self.EH._determine_type("binary.mp4"))
        self.assertTupleEqual(("GENERIC", "NOTYPE"), self.EH._determine_type("notype"))
        os.chdir("..")

    def test__find_children(self):
        def join(*args):
            return os.path.join("templates", *args) + ".html"

        base = join("base")
        extendsdeeper = join("extendsdeeper")
        l_extendsbase = join("left", "extendsbase")
        l_l_extendsbase = join("left", "left", "extendsbase")
        l_l_extendschild = join("left", "left", "extendschild")
        r_l_deeper = join("right", "left", "deeper")

        os.chdir("affected")

        golden_base = {l_extendsbase, l_l_extendsbase, l_l_extendschild}
        self.assertSetEqual(golden_base, set(self.EH._find_children(base)))

        golden_childless = set()
        self.assertSetEqual(golden_childless, set(self.EH._find_children(extendsdeeper)))

        golden_reverse = {extendsdeeper}
        self.assertSetEqual(golden_reverse, set(self.EH._find_children(r_l_deeper)))

        golden_once = {l_l_extendschild}
        self.assertSetEqual(golden_once, set(self.EH._find_children(l_extendsbase)))

        os.chdir("..")

    def test__get_affected(self):
        pass

    @patch.dict(config, {"PAGE_EXT": "md", "ROOT": {"WEB": "web", "DEV": "dev"}})
    def test__get_web_path(self):
        devroot = config["ROOT"]["DEV"]
        webroot = config["ROOT"]["WEB"]

        def join(*args):
            return os.path.join(*args)

        def get(file):
            return self.EH._get_web_path(join(devroot, file))

        self.assertEqual(join(webroot, "index.html"), get("test.md"))
        self.assertEqual(join(webroot, "generic.txt"), get("generic.txt"))
        self.assertEqual(join(webroot, "noext"), get("noext"))

    def test__get_parent_page(self):
        os.chdir("getparent")
        parent = self.EH._get_parent_page(os.path.join("_sub", "child.md"))
        self.assertEqual("parent.md", parent)

        parent = self.EH._get_parent_page("_sub")
        self.assertEqual("parent.md", parent)

        with self.assertRaises(IndexError) as context:
            self.EH._get_parent_page(os.path.join("none", "none", "parentless.md"))
        self.assertTrue("Child page has no parent!" in str(context.exception))
        os.chdir("..")

    def test__delete(self):
        os.chdir("delete")
        self.EH._delete("dir")
        self.EH._delete("nothere")
        self.EH._delete("file.txt")
        self.assertFalse(os.path.exists("dir"))
        self.assertFalse(os.path.exists("file.txt"))
        os.chdir("..")

    def test__move(self):
        def readf(path):
            with open(path, "r") as file:
                return file.read()

        os.chdir("move")

        with self.assertRaises(FileNotFoundError) as context:
            self.EH._move("nothere", "to")
        self.assertTrue("No file/dir at notification origin!" in str(context.exception))

        self.EH._move("fro.txt", "moved.txt")
        self.assertTrue(os.path.isfile("moved.txt"))
        first = readf("moved.txt")

        self.EH._move("fro2.txt", "moved.txt")
        self.assertTrue(os.path.isfile("moved.txt"))
        second = readf("moved.txt")

        self.assertNotEqual(first, second)

        self.EH._move("fro", "to")
        self.assertTrue(os.path.isdir("to"))
        self.assertTrue(os.path.isfile(os.path.join("to", "collateral")))

        self.assertFalse(os.path.exists("fro"))
        self.assertFalse(os.path.exists("fro.txt"))
        self.assertFalse(os.path.exists("fro2.txt"))

        os.chdir("..")
