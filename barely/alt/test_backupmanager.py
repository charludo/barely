import os
import time
import unittest
from ref.dircmp import is_same
from ref.utils import testdir, mkdir, remove
from barely.backup import BACKUPMANAGER as BAK


class TestBackupManager(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        bakdir = os.path.join(testdir, "backups")
        BAK.configure(os.path.join(bakdir, "devroot"),
                      os.path.join(bakdir, "webroot"),
                      os.path.join(bakdir, "backups"),
                      2)
        self.bakdir = os.path.join(bakdir, "backups")
        self.webdir = os.path.join(bakdir, "webroot")
        self.devdir = os.path.join(bakdir, "devroot")

        mkdir(bakdir)
        mkdir(os.path.join(bakdir, "devroot"))
        mkdir(os.path.join(bakdir, "webroot"))
        mkdir(os.path.join(bakdir, "backups"))

    def test_backup(self):
        time.sleep(1)
        first = BAK.backup(web=True, dev=True)
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, first[0])))
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, first[1])))

        time.sleep(1)
        second = BAK.backup(web=True, dev=True)
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, second[0])))
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, second[1])))

        time.sleep(1)
        third = BAK.backup(web=True, dev=True)
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, third[0])))
        self.assertFalse(os.path.exists(os.path.join(self.bakdir, first[0])))
        self.assertTrue(os.path.exists(os.path.join(self.bakdir, third[1])))
        self.assertFalse(os.path.exists(os.path.join(self.bakdir, first[1])))

        self.assertTrue(is_same(self.webdir, os.path.join(self.bakdir, third[0])))
        self.assertTrue(is_same(self.devdir, os.path.join(self.bakdir, third[1])))

    def test_restore(self):
        time.sleep(1)
        older = BAK.backup(web=True, dev=True)
        time.sleep(1)
        newer = BAK.backup(web=True, dev=True)

        remove(self.webdir)
        remove(self.devdir)
        mkdir(self.webdir)
        mkdir(self.devdir)

        restored_newest = BAK.restore(web=False, dev=True)
        self.assertEqual(newer[1], restored_newest[1])
        self.assertTrue(is_same(os.path.join(self.bakdir, newer[1]), self.devdir))

        restored_exact = BAK.restore(exact=older[0])
        self.assertEqual(older[0], restored_exact[0])
        self.assertTrue(is_same(os.path.join(self.bakdir, older[0]), self.webdir))
