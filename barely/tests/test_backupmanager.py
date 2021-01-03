import os
import time
import unittest
from filecmp import dircmp
from ref.utils import testdir
from barely.backup import BACKUPMANAGER as BAK


class TestBackupManager(unittest.TestCase):
    """ should be expanded to include more uncommon mk """

    @classmethod
    def setUpClass(self):
        bakdir = os.path.join(testdir, "backups")
        BAK.configure(os.path.join(bakdir, "devroot"),
                      os.path.join(bakdir, "webroot"),
                      os.path.join(bakdir, "backups"),
                      2)
        self.bakdir = os.path.join(bakdir, "backups")

    def is_same(self, left, right):
        comp = dircmp(left, right)
        if comp.left_only or comp.right_only or comp.common_funny or comp.diff_files:
            return False
        return True

    def test_backup(self):
        w_first = BAK.backup(web=True, dev=False)
        d_first = BAK.backup(web=False, dev=True)
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, w_first[0])))
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, d_first[1])))

        time.sleep(1)
        w_second = BAK.backup(web=True, dev=False)
        d_second = BAK.backup(web=False, dev=True)
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, w_second[0])))
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, d_second[1])))

        time.sleep(1)
        w_third = BAK.backup(web=True, dev=False)
        d_third = BAK.backup(web=False, dev=True)
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, w_third[0])))
        self.assertFalse(os.path.exists(os.path.join(self.bakdir, w_first[0])))
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, d_third[1])))
        self.assertFalse(os.path.exists(os.path.join(self.bakdir, d_first[1])))

        bakdir = os.path.join(testdir, "backups")
        self.assertTrue(self.is_same(os.path.join(bakdir, "webroot"), w_third))
        self.assertTrue(self.is_same(os.path.join(bakdir, "devroot"), d_third))

    def test_restore(self):
        pass
