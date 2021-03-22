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
        pass
