import os
import shutil
import unittest
from unittest.mock import MagicMock
from barely.track import CHANGETRACKER as CT
from barely.track import CHANGEHANDLER as CH
from ref.utils import touch, write, remove, testdir


class TestChangeTracker(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        CH.notify_added_file = MagicMock(name="notify_added_file")
        CH.notify_added_dir = MagicMock(name="notify_added_dir")
        CH.notify_deleted = MagicMock(name="notify_deleted")
        CH.notify_moved_file = MagicMock(name="notify_moved_file")
        CH.notify_moved_dir = MagicMock(name="notify_moved_dir")
        CH.notify_modified = MagicMock(name="notify_modified")
        CH.notify_changed_template = MagicMock(name="notify_changed_template")

        CT.setup_eventhandler(testdir)
        CT.mute()

    def loop_file_create(self):
        file = os.path.join(testdir, "file.txt")
        touch(file)

        raise KeyboardInterrupt

        remove(file)

        self.assertTrue(CH.notify_added_file.called)
        self.assertFalse(CH.notify_added_dir.called)
        self.assertFalse(CH.notify_moved_file.called)
        self.assertFalse(CH.notify_moved_dir.called)
        self.assertFalse(CH.notify_modified.called)
        self.assertFalse(CH.notify_deleted.called)
        self.assertFalse(CH.notify_changed_template.called)

        return True

    def loop_dir_create(self):
        dir = os.path.join(testdir, "dir/")
        os.mkdir(dir)
        raise KeyboardInterrupt

        remove(dir)

        self.assertFalse(CH.notify_added_file.called)
        self.assertTrue(CH.notify_added_dir.called)
        self.assertFalse(CH.notify_moved_file.called)
        self.assertFalse(CH.notify_moved_dir.called)
        self.assertFalse(CH.notify_modified.called)
        self.assertFalse(CH.notify_deleted.called)
        self.assertFalse(CH.notify_changed_template.called)

        return True

    def loop_file_move(self):
        shutil.move(os.path.join(testdir, "file.txt"), os.path.join(testdir, "moved.txt"))

        raise KeyboardInterrupt

        remove(os.path.join(testdir, "moved.txt"))

        self.assertFalse(CH.notify_added_file.called)
        self.assertFalse(CH.notify_added_dir.called)
        self.assertTrue(CH.notify_moved_file.called)
        self.assertFalse(CH.notify_moved_dir.called)
        self.assertFalse(CH.notify_modified.called)
        self.assertFalse(CH.notify_deleted.called)
        self.assertFalse(CH.notify_changed_template.called)

        return True

    def loop_dir_move(self):
        shutil.move(os.path.join(testdir, "dir/"), os.path.join(testdir, "moved/"))

        raise KeyboardInterrupt

        remove(os.path.join(testdir, "moved/"))

        self.assertFalse(CH.notify_added_file.called)
        self.assertFalse(CH.notify_added_dir.called)
        self.assertFalse(CH.notify_moved_file.called)
        self.assertTrue(CH.notify_moved_dir.called)
        self.assertFalse(CH.notify_modified.called)
        self.assertFalse(CH.notify_deleted.called)
        self.assertFalse(CH.notify_changed_template.called)

        return True

    def loop_file_delete(self):
        remove(os.path.join(testdir, "file.txt"))

        raise KeyboardInterrupt

        self.assertFalse(CH.notify_added_file.called)
        self.assertFalse(CH.notify_added_dir.called)
        self.assertFalse(CH.notify_moved_file.called)
        self.assertFalse(CH.notify_moved_dir.called)
        self.assertFalse(CH.notify_modified.called)
        self.assertTrue(CH.notify_deleted.called)
        self.assertFalse(CH.notify_changed_template.called)

        return True

    def loop_dir_delete(self):
        remove(os.path.join(testdir, "dir/"))

        raise KeyboardInterrupt

        self.assertFalse(CH.notify_added_file.called)
        self.assertFalse(CH.notify_added_dir.called)
        self.assertFalse(CH.notify_moved_file.called)
        self.assertFalse(CH.notify_moved_dir.called)
        self.assertFalse(CH.notify_modified.called)
        self.assertTrue(CH.notify_deleted.called)
        self.assertFalse(CH.notify_changed_template.called)

        return True

    def loop_modified(self):
        write("file.txt", "test")

        raise KeyboardInterrupt

        remove(os.path.join(testdir, "file.txt"))

        self.assertFalse(CH.notify_added_file.called)
        self.assertFalse(CH.notify_added_dir.called)
        self.assertFalse(CH.notify_moved_file.called)
        self.assertFalse(CH.notify_moved_dir.called)
        self.assertTrue(CH.notify_modified.called)
        self.assertFalse(CH.notify_deleted.called)
        self.assertFalse(CH.notify_changed_template.called)

        return True

    def loop_templates(self):
        touch(os.path.join(testdir, "templates", "test.html"))

        raise KeyboardInterrupt

        remove(os.path.join(testdir, "templates", "test.html"))

        self.assertFalse(CH.notify_added_file.called)
        self.assertFalse(CH.notify_added_dir.called)
        self.assertFalse(CH.notify_moved_file.called)
        self.assertFalse(CH.notify_moved_dir.called)
        self.assertFalse(CH.notify_modified.called)
        self.assertFalse(CH.notify_deleted.called)
        self.assertTrue(CH.notify_changed_template.called)

        return True

    def test__notify(self):

        done = True
        if done:
            done = CT.start(loop_action=self.loop_file_create)
        if done:
            done = CT.start(loop_action=self.loop_dir_create)
        if done:
            touch(os.path.join(testdir, "file.txt"))
            done = CT.start(loop_action=self.loop_file_move)
        if done:
            os.mkdir(os.path.join(testdir, "dir/"))
            done = CT.start(loop_action=self.loop_dir_move)
        if done:
            touch(os.path.join(testdir, "file.txt"))
            done = CT.start(loop_action=self.loop_file_delete)
        if done:
            os.mkdir(os.path.join(testdir, "dir/"))
            done = CT.start(loop_action=self.loop_dir_delete)
        if done:
            touch(os.path.join(testdir, "file.txt"))
            done = CT.start(loop_action=self.loop_modified)
        if done:
            done = CT.start(loop_action=self.loop_templates)
