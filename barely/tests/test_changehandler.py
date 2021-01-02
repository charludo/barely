import os
import unittest
from barely.track import changehandler
from ref.utils import remove, testdir, touch
from barely.render import RENDERER as R


class TestChangeHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ch = changehandler.ChangeHandler.instance()
        self.dir = os.path.join(testdir, "dir/")
        self.file = os.path.join(testdir, "file.txt")

        R.set_template_path(os.path.join(testdir, "templates/"))

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
        self.assertEqual(message, f"created: {self.dir} ")

    def test_notify_deleted(self):
        os.mkdir(self.dir)
        touch(self.file)

        message = self.ch.notify_deleted(self.file)
        self.assertFalse(os.path.exists(self.file))
        self.assertEqual(message, f"deleted: {self.file} ")

        message = self.ch.notify_deleted(self.dir)
        self.assertFalse(os.path.exists(self.dir))
        self.assertEqual(message, f"deleted: {self.dir} ")

    def test_notify_moved_file(self):
        pass

    def test_notify_moved_dir(self):
        os.mkdir(self.dir)
        newdir = os.path.join(testdir, "new/")

        message = self.ch.notify_moved_dir(self.dir, newdir)
        self.assertFalse(os.path.exists(self.dir))
        self.assertTrue(os.path.exists(newdir))
        self.assertEqual(message, f"moved: {self.dir} to: {newdir}")

        remove(newdir)

    def test_notify_modified(self):
        # renderable (.md)
        f_in = os.path.join(testdir, "in.md")
        f_out = os.path.join(testdir, "index.html")
        touch(f_in)
        message = self.ch.notify_modified(f_in, f_out)

        self.assertTrue(os.path.exists(f_out))
        self.assertTrue(os.path.exists(f_in))
        self.assertEqual(message, f"updated: {f_out} ")
        remove(f_in)
        remove(f_out)

        # compressable (.js)
        f_in = os.path.join(testdir, "test.js")
        f_out = os.path.join(testdir, "test.min.js")
        touch(f_in)
        message = self.ch.notify_modified(f_in, f_out)

        # self.assertTrue(os.path.exists(f_out))
        self.assertTrue(os.path.exists(f_in))
        self.assertEqual(message, f"updated: {f_out} ")
        remove(f_in)
        remove(f_out)

        # compressable (.css)
        f_in = os.path.join(testdir, "test.scss")
        f_out = os.path.join(testdir, "test.min.css")
        touch(f_in)
        message = self.ch.notify_modified(f_in, f_out)

        # self.assertTrue(os.path.exists(f_out))
        self.assertTrue(os.path.exists(f_in))
        self.assertEqual(message, f"updated: {f_out} ")
        remove(f_in)
        remove(f_out)

        # compressable (img)
        f_in = os.path.join(testdir, "test.jpg")
        f_out = os.path.join(testdir, "testmin.jpg")
        touch(f_in)
        message = self.ch.notify_modified(f_in, f_out)

        # self.assertTrue(os.path.exists(f_out))
        self.assertTrue(os.path.exists(f_in))
        self.assertEqual(message, f"updated: {f_out} ")
        remove(f_in)
        remove(f_out)

        # everything else
        f_in = os.path.join(testdir, "test.txt")
        f_out = os.path.join(testdir, "testcopy.txt")
        touch(f_in)
        message = self.ch.notify_modified(f_in, f_out)

        self.assertTrue(os.path.exists(f_out))
        self.assertTrue(os.path.exists(f_in))
        self.assertEqual(message, f"updated: {f_out} ")
        remove(f_in)
        remove(f_out)
