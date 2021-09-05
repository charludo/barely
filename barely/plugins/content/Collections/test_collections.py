import os
import unittest
from mock import patch
from unittest.mock import MagicMock
from barely.plugins.content.Collections.collections import Collections


class TestCollections(unittest.TestCase):

    maxDiff = None

    @patch("barely.plugins.content.Collections.collections.splitext")
    @patch("barely.plugins.content.Collections.collections.join")
    @patch("barely.plugins.content.Collections.collections.walk")
    @patch("barely.plugins.content.Collections.collections.read_file")
    @patch("barely.plugins.content.Collections.collections.parse_meta")
    @patch("barely.plugins.content.Collections.collections.Collections.action")
    def test___init__(self, action, parse_meta, read_file, walk, join, splitext):

        col = Collections()
        self.assertDictEqual({"PRIORITY": -1}, col.plugin_config)

        walk.__iter__.side_effect = lambda x, topdown: "", "", ["template.md"]
        splitext.return_value = ["template", "md"]
        join.return_value = "template.md"
        parse_meta.return_value = {}

        golden = {
            "PRIORITY": 2,
            "PAGE": "categories",
            "OVERVIEW_TITLE": "",
            "OVERVIEW_TEMPLATE": "",
            "COLLECTION_TEMPLATE": "",
            "SUMMARY_LENGTH": 100
        }
        col.config["COLLECTIONS"] = {"PRIORITY": 2}
        col.__init__()

        self.assertDictEqual(golden, col.plugin_config)
        self.assertTrue(parse_meta.called_with("template.md"))

        # reset
        del col.config["COLLECTIONS"]
        col.COLLECTION = {}
        col.EXHIBITS = set()
        col.__init__()

    def test_register(self):
        col = Collections()
        name, prio, ext = col.register()

        self.assertEqual(name, "Collections")
        self.assertEqual(prio, -1)
        self.assertEqual(ext, ["md"])

    @patch("barely.plugins.content.Collections.collections.write_file")
    @patch("barely.plugins.content.Collections.collections.render_page")
    @patch("barely.plugins.content.Collections.collections.parse_meta")
    @patch("barely.plugins.content.Collections.collections.hook_plugins")
    @patch("barely.plugins.content.Collections.collections.EH")
    @patch("barely.plugins.content.Collections.collections.getmtime")
    def test_action_and_finalize(self, getmtime, EH, hook_plugins, parse_meta, render_page, write_file):
        item_1 = {
            "meta": {
                "title": "Test",
                "title_image": "dir/img.png",
                "created": "21.07.2021",
                "reading_time": "1 - 3",
                "collections": ["col1", "col2"]
            },
            "content": "contents of this page, deliberatly < 100 chars",
            "content_raw": "contents of this page, deliberatly < 100 chars",
            "destination": "web/page/page.html",
            "origin": "./page/page.md"
        }

        item_2 = {
            "meta": {
                "title": "Test 2",
                "title_image": "dir/img.png",
                "created": "10.07.2021",
                "reading_time": "1 - 3",
                "collections": ["col2", "col3"],
                "exhibits": ["col1", "col4"]
            },
            "content": "contents of this page, deliberatly < 100 chars",
            "content_raw": "contents of this page, deliberatly < 100 chars",
            "destination": "web/page2/page2.html",
            "origin": "./page2/page2.md"
        }

        getmtime.return_value = 2

        col = Collections()
        old_root = col.config["ROOT"]["DEV"]
        col.config["ROOT"]["DEV"] = os.path.join(old_root, "empty")
        col.config["COLLECTIONS"] = {"PRIORITY": 2}
        col.__init__()

        self.assertDictEqual({}, col.COLLECTION)
        self.assertSetEqual(set(), col.EXHIBITS)

        result_1 = list(col.action(item=item_1.copy()))[0]
        result_1b = list(col.action(item=item_1.copy()))[0]
        result_2 = list(col.action(item=item_2.copy()))[0]

        collectible_1 = {
            "title": "Test",
            "image": "dir/img.png",
            "date": "21.07.2021",
            "reading_time": "1 - 3",
            "preview": "contents of this page, deliberatly < 100 chars...",
            "raw": "contents of this page, deliberatly < 100 chars",
            "href": "/page/page.html",
            "timestamp": 2
        }
        collectible_2 = {
            "title": "Test 2",
            "image": "dir/img.png",
            "date": "10.07.2021",
            "reading_time": "1 - 3",
            "preview": "contents of this page, deliberatly < 100 chars...",
            "raw": "contents of this page, deliberatly < 100 chars",
            "href": "/page2/page2.html",
            "timestamp": 2
        }
        golden_collection = {
            "col1": [collectible_1],
            "col2": [collectible_1, collectible_2],
            "col3": [collectible_2]
        }
        self.assertDictEqual(golden_collection, col.COLLECTION)

        item_2["meta"]["exhibits"] = {
            "col2": [collectible_1, collectible_2],
            "col4": []
        }
        golden_exhibits = set(["./page2/page2.md"])
        self.assertSetEqual(golden_exhibits, col.EXHIBITS)

        self.assertDictEqual(item_1, result_1)
        self.assertDictEqual(item_1, result_1b)
        self.assertDictEqual(item_2, result_2)

        #
        #   FINALIZE
        #

        EH.notify = MagicMock()

        col.plugin_config["OVERVIEW_TITLE"] = "overview"
        col.plugin_config["OVERVIEW_TEMPLATE"] = "placeholder-overview"
        col.plugin_config["COLLECTION_TEMPLATE"] = "placeholder"

        col.finalize()
        col.config["ROOT"]["DEV"] = old_root

        golden_args = [
            {
                "template": "placeholder",
                "destination": os.path.join("web", "categories", "col1", "index.html"),
                "meta": {
                    "title": "col1",
                    "collectibles": [collectible_1]
                },
                "content": "",
                "content_raw": "",
                "action": "collected",
                "origin": "col1",
                "extension": "md"
            },
            {
                "template": "placeholder",
                "destination": os.path.join("web", "categories", "col2", "index.html"),
                "meta": {
                    "title": "col2",
                    "collectibles": [collectible_1, collectible_2]
                },
                "content": "",
                "content_raw": "",
                "action": "collected",
                "origin": "col2",
                "extension": "md"
            },
            {
                "template": "placeholder",
                "destination": os.path.join("web", "categories", "col3", "index.html"),
                "meta": {
                    "title": "col3",
                    "collectibles": [collectible_2]
                },
                "content": "",
                "content_raw": "",
                "action": "collected",
                "origin": "col3",
                "extension": "md"
            },
            {
                "template": "placeholder-overview",
                "destination": os.path.join("web", "categories", "index.html"),
                "meta": {
                    "title": "overview",
                    "collections": [
                        {
                            "name": "col2",
                            "size": 2,
                            "href": "/categories/col2/index.html"
                        },
                        {
                            "name": "col1",
                            "size": 1,
                            "href": "/categories/col1/index.html"
                        },
                        {
                            "name": "col3",
                            "size": 1,
                            "href": "/categories/col3/index.html"
                        }
                    ]
                },
                "content": "",
                "content_raw": "",
                "action": "created overview",
                "origin": "all collections",
                "extension": "md"
            }
        ]
        actual_args = [list(args[0])[0] for args, kwargs in parse_meta.call_args_list]
        self.assertCountEqual(golden_args, actual_args)

        del col.config["COLLECTIONS"]
        col.COLLECTION = {}
        col.EXHIBITS = set()
        col.__init__()
