import os
import unittest
from barely.track import changehandler
from ref.utils import remove, testdir, touch, write, read
from barely.render import RENDERER as R


class TestChangeHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ch = changehandler.ChangeHandler.instance()
        self.dir = os.path.join(testdir, "dir/")
        self.file = os.path.join(testdir, "file.txt")

        R.set_template_path(os.path.join(testdir, "templates/"))

    def tearDown(self):
        remove(self.dir)
        remove(self.file)

    def _update_test_helper(self, dev, web, action, message_from):
        write(dev, "updated content")
        write(web, "old content")
        self.assertEqual(read(web), "old content")

        message_from = os.path.join(testdir, message_from)
        expected_message = f"{action}: {message_from} "

        message = self.ch.notify_modified(os.path.join(testdir, dev), os.path.join(testdir, web))
        self.assertEqual(message, expected_message)
        self.assertNotEqual(read(web), "old content")

        remove(os.path.join(testdir, dev))
        remove(os.path.join(testdir, web))

    def test_notify_added_file(self):
        """doesn"t test for correctly rendering / compressing /
        ... since that's been taken care of in the
        test_notify_modified function"""

        touch(self.file)
        webfile = os.path.join(testdir, "webfile.txt")

        message = self.ch.notify_added_file(self.file, webfile)

        self.assertTrue(os.path.exists(webfile))
        self.assertEqual(message, f"created: {webfile} ")

        remove(webfile)

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
        """doesn"t test for correctly rendering / compressing /
        ... since that's been taken care of in the
        test_notify_modified function"""

        newfile = os.path.join(testdir, "filenew.txt")
        movedfile = os.path.join(testdir, "filemoved.txt")
        touch(self.file)
        touch(newfile)

        message = self.ch.notify_moved_file(self.file, newfile, movedfile)

        self.assertTrue(os.path.exists(movedfile))
        self.assertFalse(os.path.exists(self.file))
        self.assertEqual(message, f"moved: {self.file} to: {movedfile}")

        remove(newfile)
        remove(movedfile)

    def test_notify_moved_dir(self):
        os.mkdir(self.dir)
        newdir = os.path.join(testdir, "new/")

        message = self.ch.notify_moved_dir(self.dir, newdir)
        self.assertFalse(os.path.exists(self.dir))
        self.assertTrue(os.path.exists(newdir))
        self.assertEqual(message, f"moved: {self.dir} to: {newdir}")

        remove(newdir)

    def test_notify_modified(self):
        # missing: images
        self._update_test_helper("in.md",  "index.html", "updated", "index.html")
        self._update_test_helper("a.css",  "a.min.css", "updated", "a.min.css")
        self._update_test_helper("a.js",  "a.min.js", "updated", "a.min.js")
        self._update_test_helper("dev.txt",  "web.txt", "updated", "web.txt")
