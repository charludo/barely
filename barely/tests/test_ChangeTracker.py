import unittest
from mock import patch
from unittest.mock import MagicMock
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from barely.core.ChangeTracker import ChangeTracker


class TestChangeTracker(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        with patch.object(ChangeTracker, "__init__", lambda x: None):
            self.CT = ChangeTracker()

    def test___init__(self):
        EH_no = ChangeTracker()
        self.assertFalse(EH_no.handler_available)

        with patch("barely.core.ChangeTracker.ChangeTracker.register_handler") as reg:
            ChangeTracker(lambda x: x)
        self.assertTrue(reg.called)

    def test_register_handler(self):
        with patch.object(PatternMatchingEventHandler, "__init__", lambda v, w, x, y, z: None):
            with patch.object(Observer, "schedule") as obs:
                self.CT.register_handler(lambda x: None)
                self.assertTrue(obs.called)

    """def test_track(self):
        self.CT.handler_available = False
        with self.assertRaises(Exception) as context:
            self.CT.track()
        self.assertTrue("No available handler. Not tracking." in str(context.exception))

        self.CT.handler_available = True
        self.CT.observer = Observer()
        self.CT.observer.start = MagicMock()
        self.CT.observer.stop = MagicMock()
        self.CT.observer.join = MagicMock()

        def loop_action():
            raise KeyboardInterrupt
        self.CT.track(loop_action)

        self.assertTrue(self.CT.observer.start.called)
        self.assertTrue(self.CT.observer.stop.called)
        self.assertTrue(self.CT.observer.join.called)"""

    def test_buffer(self):
        pass

    def test_empty_buffer(self):
        pass

    @patch("signal.signal")
    @patch("multiprocessing.Process")
    @patch("watchdog.observers.Observer")
    def test_stop(self, observer, liveserver, signal):
        self.CT.observer = observer
        self.CT.observer.stop = MagicMock()
        self.CT.observer.join = MagicMock()
        self.CT.liveserver = liveserver
        self.CT.liveserver.join = MagicMock()
        self.CT.tracking = True
        self.CT.original_sigint = None

        self.CT.stop(None, None)

        self.assertTrue(self.CT.observer.stop.called)
        self.assertTrue(self.CT.observer.join.called)
        self.assertTrue(self.CT.liveserver.join.called)
        self.assertTrue(signal.called)
        self.assertFalse(self.CT.tracking)
