import unittest
from mock import patch
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from barely.core.ChangeTracker import ChangeTracker


class TestChangeTracker(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        with patch.object(ChangeTracker, "__init__", lambda x: None):
            self.CT = ChangeTracker.instance()

    def test_register_handler(self):
        with patch.object(PatternMatchingEventHandler, "__init__", lambda v, w, x, y, z: None):
            with patch.object(Observer, "schedule") as obs:
                self.CT.register_handler(lambda x: None)
                self.assertTrue(obs.called)

    def test_track(self):
        pass
