import os
import unittest
from mock import patch
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
        pass

    def test__find_children(self):
        pass

    def test__get_affected(self):
        pass

    def test__get_web_path(self):
        pass

    def test__get_parent_page(self):
        pass

    def test__delete(self):
        pass

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
