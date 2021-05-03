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

    @patch("signal.getsignal")
    @patch("signal.signal")
    @patch("livereload.Server")
    @patch("multiprocessing.Process")
    @patch("watchdog.observers.Observer")
    def test_track(self, observer, server, serverprocess, signal, getsignal):
        self.CT.handler_available = False
        with self.assertRaises(Exception) as context:
            self.CT.track()
        self.assertTrue("No available handler. Not tracking." in str(context.exception))

        self.CT.verbose = False
        self.CT.handler_available = True
        self.CT.observer = observer
        self.CT.observer.start = MagicMock()
        self.CT.liveserver.start = MagicMock()
        serverprocess.start = MagicMock()
        server.serve = MagicMock()
        server.watch = MagicMock()
        getsignal.return_value = None

        def loop_action():
            self.CT.tracking = False
        with patch("barely.core.ChangeTracker.ChangeTracker.empty_buffer"):
            self.CT.track(loop_action)
        self.CT.liveserver.kill()
        self.assertTrue(self.CT.observer.start.called)
        self.assertTrue(signal.called)
        self.assertTrue(getsignal.called)
        self.assertTrue(server.watch)

    def test_buffer(self):
        self.CT.eventbuffer = []

        event_1a = type('obj', (object,), {"src_path": 1})
        event_1b = type('obj', (object,), {"dest_path": 1, "src_path": 123})
        event_2 = type('obj', (object,), {"src_path": 2})

        self.CT.buffer(event_1a)
        self.CT.buffer(event_2)
        self.CT.buffer(event_1b)

        self.assertEqual(2, len(self.CT.eventbuffer))
        self.assertEqual(2, self.CT.eventbuffer[0].src_path)
        self.assertEqual(2, self.CT.eventbuffer[0].relevant_path)
        self.assertEqual(1, self.CT.eventbuffer[1].dest_path)
        self.assertEqual(1, self.CT.eventbuffer[1].relevant_path)

    @patch("barely.core.EventHandler.EventHandler")
    def test_empty_buffer(self, EH):
        def enbuffer(item):
            emptied_buffer.append(item)
        emptied_buffer = []
        original_buffer = [1, 2, 3]

        self.CT.EH = EH
        self.CT.EH.notify = MagicMock(side_effect=enbuffer)
        self.CT.eventbuffer = original_buffer.copy()

        self.CT.empty_buffer()

        self.assertListEqual(original_buffer, emptied_buffer)
        self.assertListEqual([], self.CT.eventbuffer)

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
