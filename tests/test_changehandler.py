import os
import unittest
from src import changehandler
from ref.utils import read, prepare_tempfiles, cleanup, remove


class TestChangeHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ch = changehandler.ChangeHandler()
        self.dir = os.path.join("test", "ref", "dir/")
        self.file = os.path.join("test", "ref", "file.txt")

    @classmethod
    def tearDownClass(self):
        self.ch = None
        del self.ch

    def tearDown(self):
        remove(self.dir)
        remove(self.file)

    def test_notify_added_file(self):
        pass

    def test_notify_added_dir(self):
        message = self.ch.notify_added_dir(self.dir)
        self.assertTrue(os.path.exists(self.dir))
        self.assertEqual(message, "created: test/ref/dir/ ")

    def test_notify_deleted(self):
        os.mkdir(self.dir)
        open(self.file, "x")

        message = self.ch.notify_deleted(self.file)
        self.assertFalse(os.path.exists(self.file))
        self.assertEqual(message, "deleted: test/ref/file.txt ")

        message = self.ch.notify_deleted(self.dir)
        self.assertFalse(os.path.exists(self.dir))
        self.assertEqual(message, "deleted: test/ref/dir/ ")

    def test_notify_moved_file(self):
        pass

    def test_notify_moved_dir(self):
        pass

    def test_notify_modified(self):
        pass
