import os
import unittest
from mock import patch
from barely.common.config import config
from barely.core.EventHandler import EventHandler
from watchdog.events import FileCreatedEvent, FileModifiedEvent
from watchdog.events import FileDeletedEvent, DirModifiedEvent
from watchdog.events import FileMovedEvent, DirMovedEvent


class TestEventHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.chdir("EventHandler")
        self.EH = EventHandler()

    @classmethod
    def tearDownClass(self):
        os.chdir("..")

    @patch("barely.core.ProcessingPipeline.init_jinja")
    def test_init_pipeline(self, jinja):
        self.EH.init_pipeline(1)
        self.assertTrue(jinja.called)

    @patch("barely.core.ProcessingPipeline.process")
    @patch("barely.core.EventHandler.EventHandler._determine_type")
    @patch("barely.core.ProcessingPipeline.move")
    @patch("barely.core.ProcessingPipeline.delete")
    @patch("barely.core.EventHandler.EventHandler._get_parent_page")
    @patch("barely.core.EventHandler.EventHandler._get_affected")
    @patch("barely.core.EventHandler.EventHandler._get_web_path")
    def test_notify(self, _get_web_path, _get_affected, _get_parent_page, delete, move, _determine_type, process):
        def join(*args):
            return os.path.join(*args)

        def catch_response(response):
            response_items.append(response[0])
        response_items = []

        # a bit counterintuitive, but easier to test:
        # only the origin ever changes with these mocks
        _get_web_path.return_value = "destination"
        _get_affected.side_effect = lambda x: [x[10:]]
        _get_parent_page.return_value = "parent"
        delete.return_value = None
        move.return_value = None
        _determine_type.return_value = ("TYPE", "ext")
        process.side_effect = catch_response

        golden_item = {
            "origin": "origin",
            "destination": "destination",
            "type": "TYPE",
            "extension": "ext"
        }

        # template modified
        golden_item["origin"] = "tpl"
        self.EH.notify(FileModifiedEvent(src_path=join("templates", "tpl")))
        self.assertDictEqual(golden_item, response_items[-1])

        # template moved
        golden_item["origin"] = "dest"
        self.EH.notify(FileMovedEvent(src_path=join("templates", "origin"), dest_path=join("templates", "dest")))
        self.assertDictEqual(golden_item, response_items[-1])

        # metadata.yaml
        golden_item["origin"] = ""
        self.EH.notify(FileModifiedEvent(src_path="metadata.yaml"))
        self.assertDictEqual(golden_item, response_items[-1])

        # subpage
        golden_item["origin"] = "parent"
        self.EH.notify(FileModifiedEvent(src_path=join("", "_subpage", "origin.md")))
        self.assertDictEqual(golden_item, response_items[-1])

        # deleted
        self.EH.notify(FileDeletedEvent(src_path="trash"))
        self.assertTrue(delete.called)

        # moved
        _get_web_path.side_effect = lambda x: x
        self.EH.notify(DirMovedEvent(src_path="from", dest_path="to"))
        self.assertTrue(move.called)
        _get_web_path.side_effect = None

        # created file
        golden_item["origin"] = "file.png"
        self.EH.notify(FileCreatedEvent(src_path="file.png"))
        self.assertDictEqual(golden_item, response_items[-1])

        # config.yaml, .git (other/pointless)
        self.EH.notify(FileModifiedEvent(src_path="config.yaml"))
        self.EH.notify(FileModifiedEvent(src_path=".git"))

        # DirModifiedEvent (other/pointless)
        self.EH.notify(DirModifiedEvent(src_path="dir"))

        # number of unique responses we should have received
        self.assertEqual(5, len(list({r["origin"]: r for r in response_items}.values())))

    @patch("barely.core.EventHandler.EventHandler.notify")
    def test_force_rebuild(self, notify):
        notifications = []

        def collect_notifications(notification):
            notifications.append(notification.src_path)

        os.chdir("force")

        notify.side_effect = collect_notifications
        self.EH.force_rebuild("devroot")

        golden_notified = {
            os.path.join(".", "dir", "_subpage", "subimage.jpg"),
            os.path.join(".", "dir", "page.md"),
            os.path.join(".", "dir", "image.png"),
            os.path.join(".", "file.txt")
        }
        self.assertSetEqual(golden_notified, set(notifications))

        notifications = []
        self.EH.force_rebuild("dir")
        golden_notified = {
            os.path.join(".", "dir", "_subpage", "subimage.jpg"),
            os.path.join(".", "dir", "page.md"),
            os.path.join(".", "dir", "image.png"),
        }
        self.assertSetEqual(golden_notified, set(notifications))

        self.EH.force_rebuild(os.path.join(".", "dir"))
        self.assertSetEqual(golden_notified, set(notifications))

        notifications = []
        self.EH.force_rebuild("file.txt")
        golden_notified = {
            os.path.join(".", "file.txt")
        }
        self.assertSetEqual(golden_notified, set(notifications))

        notifications = []
        self.EH.force_rebuild("devroot", True)
        golden_notified = {
            os.path.join(".", "dir", "page.md"),
            os.path.join(".", "file.txt")
        }
        self.assertSetEqual(golden_notified, set(notifications))

        os.chdir("..")

    @patch.dict(config, {"ROOT": {"DEV": "." + os.sep, "WEB": ""}, "PAGE_EXT": "md"})
    @patch("barely.core.EventHandler.EventHandler._find_children")
    def test__get_affected(self, _f_c):
        def join(*args):
            return os.path.join("templates", *args)

        base = join("base.html")
        l_r_completelyalone = join("left", "right", "completelyalone.html")
        l_l = join("left", "left")

        os.chdir("affected")
        _f_c.return_value = []
        self.assertSetEqual({"base.md"}, set(self.EH._get_affected(base)))
        self.assertSetEqual({"left.right.completelyalone.md"}, set(self.EH._get_affected(l_r_completelyalone)))
        self.assertSetEqual({"left.left.extendsbase.md", "left.left.extendschild.md"}, set(self.EH._get_affected(l_l)))

        os.chdir("..")

    def test__find_children(self):
        def join(*args):
            return os.path.join("templates", *args) + ".html"

        base = join("base")
        extendsdeeper = join("extendsdeeper")
        l_extendsbase = join("left", "extendsbase")
        l_parentless = join("left", "parentless")
        l_l_extendsbase = join("left", "left", "extendsbase")
        l_l_extendschild = join("left", "left", "extendschild")
        r_l_deeper = join("right", "left", "deeper")
        r_r_extendsparentless = join("right", "right", "extendsparentless")

        os.chdir("affected")

        golden_base = {l_extendsbase, l_l_extendsbase, l_l_extendschild}
        self.assertSetEqual(golden_base, set(self.EH._find_children(base)))

        golden_parentless = {l_extendsbase, r_r_extendsparentless, l_l_extendschild}
        self.assertSetEqual(golden_parentless, set(self.EH._find_children(l_parentless)))

        golden_childless = set()
        self.assertSetEqual(golden_childless, set(self.EH._find_children(extendsdeeper)))

        golden_reverse = {extendsdeeper}
        self.assertSetEqual(golden_reverse, set(self.EH._find_children(r_l_deeper)))

        golden_once = {l_l_extendschild}
        self.assertSetEqual(golden_once, set(self.EH._find_children(l_extendsbase)))

        os.chdir("..")

    def test__determine_type(self):
        os.chdir("type")
        self.assertTupleEqual(("PAGE", "md"), self.EH._determine_type("file.md"))
        self.assertTupleEqual(("IMAGE", "png"), self.EH._determine_type("file.png"))
        self.assertTupleEqual(("TEXT", "css"), self.EH._determine_type("file.css"))
        self.assertTupleEqual(("GENERIC", "mp4"), self.EH._determine_type("binary.mp4"))
        self.assertTupleEqual(("GENERIC", "NOTYPE"), self.EH._determine_type("notype"))
        os.chdir("..")

    @patch.dict(config, {"PAGE_EXT": "md", "ROOT": {"WEB": "web", "DEV": "dev"}})
    def test__get_web_path(self):
        devroot = config["ROOT"]["DEV"]
        webroot = config["ROOT"]["WEB"]

        def join(*args):
            return os.path.join(*args)

        def get(file):
            return self.EH._get_web_path(join(devroot, file))

        self.assertEqual(join(webroot, "index.html"), get("test.md"))
        self.assertEqual(join(webroot, "generic.txt"), get("generic.txt"))
        self.assertEqual(join(webroot, "noext"), get("noext"))

    def test__get_parent_page(self):
        os.chdir("getparent")
        parent = self.EH._get_parent_page(os.path.join("_sub", "child.md"))
        self.assertEqual("parent.md", parent)

        parent = self.EH._get_parent_page("_sub")
        self.assertEqual("parent.md", parent)

        with self.assertRaises(IndexError) as context:
            self.EH._get_parent_page(os.path.join("none", "none", "parentless.md"))
        self.assertTrue("Child page has no parent!" in str(context.exception))
        os.chdir("..")
