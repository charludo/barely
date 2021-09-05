import os
import unittest
from mock import patch
from unittest.mock import MagicMock
from PIL.PngImagePlugin import PngImageFile
from PIL import Image, ImageChops, UnidentifiedImageError
import barely.core.ProcessingPipeline as PP
from barely.plugins.PluginManager import PluginManager


class TestProcessingPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.chdir("ProcessingPipeline")

        self.item = {
            "origin": "xxx",
            "destination": "",
            "type": "",
            "extension": ""
        }
        PP.init_jinja()
        with patch.object(PluginManager, "__init__", lambda x: None):
            PP.PM = PluginManager()
            PP.PM.hook_content = MagicMock(side_effect=lambda x: [x])

    @classmethod
    def tearDownClass(self):
        os.chdir("..")

    def test_init_plugin_manager(self):
        current_PM = PP.PM
        PP.init_plugin_manager(1)
        new_PM = PP.PM
        PP.init_plugin_manager(current_PM)
        self.assertNotEqual(current_PM, new_PM)

    def test_init_jinja(self):
        current_jinja = PP.jinja
        PP.init_jinja()
        new_jinja = PP.jinja
        self.assertNotEqual(current_jinja, new_jinja)

    def test_process(self):
        with patch("barely.core.ProcessingPipeline.pipe_page") as pipe_page:
            item = {
                "type": "PAGE"
            }
            PP.process([self.item | item])
            self.assertTrue(pipe_page.called)

        with patch("barely.core.ProcessingPipeline.pipe_image") as pipe_image:
            item = {
                "type": "IMAGE"
            }
            PP.process([self.item | item])
            self.assertTrue(pipe_image.called)

        with patch("barely.core.ProcessingPipeline.pipe_text") as pipe_text:
            item = {
                "type": "TEXT"
            }
            PP.process([self.item | item])
            self.assertTrue(pipe_text.called)

        with patch("barely.core.ProcessingPipeline.pipe_generic") as pipe_generic:
            item = {
                "type": "GENERIC"
            }
            PP.process([self.item | item])
            self.assertTrue(pipe_generic.called)

        self.assertRaises(TypeError, PP.process, 0)
        self.assertRaises(ValueError, PP.process, self.item)
        self.assertRaises(ValueError, PP.process, {})

    def test_pipe_page(self):
        PP.init_jinja()

        golden_render = "a\n<h1>Title</h1>\n"

        item = {
            "origin": "pipes/page_dev.md",
            "destination": "pipes/page_web.html",
            "action": ""
        }

        PP.pipe_page([item])
        with open("pipes/page_web.html", "r") as file:
            rendered = file.read()
        self.assertEqual(golden_render, rendered)

        # with a subpage:
        golden_render = "<h1>Title Parent</h1>\n\n\n<p>Child</p>\n\npm"
        item = {
            "origin": "pipes/page_with_child_dev.md",
            "destination": "pipes/page_with_child_web.html",
            "action": ""
        }

        PP.pipe_page([item])
        with open("pipes/page_with_child_web.html", "r") as file:
            rendered = file.read()
        self.assertEqual(golden_render, rendered)

    def test_pipe_image(self):
        def loadi(path):
            return Image.open(path)

        item = {
            "origin": "pipes/image_dev.png",
            "destination": "pipes/image_web.png",
            "action": "",
            "extension": "png"
        }
        PP.pipe_image([item])
        self.assertFalse(ImageChops.difference(loadi("pipes/image_dev.png"), loadi("pipes/image_web.png")).getbbox())

    def test_pipe_text(self):
        def readf(path):
            with open(path, "r") as file:
                return file.read()

        item = {
            "origin": "pipes/text_dev.txt",
            "destination": "pipes/text_web.txt",
            "action": ""
        }
        PP.pipe_text([item])
        self.assertEqual(readf("pipes/text_dev.txt"), readf("pipes/text_web.txt"))

    def test_pipe_generic(self):
        def readf(path):
            with open(path, "r") as file:
                return file.read()

        item = {
            "origin": "pipes/generic_dev.txt",
            "destination": "pipes/generic_web.txt",
            "action": ""
        }
        PP.pipe_generic([item])
        self.assertEqual(readf("pipes/generic_dev.txt"), readf("pipes/generic_web.txt"))

    def test_pipe_subpage(self):
        golden_render = "a\n<h1>Title</h1>\n\n"

        item = {
            "origin": "pipes/subpage_dev.md",
        }

        PP.init_jinja()
        rendered = list(PP.pipe_subpage([item]))[0]["output"]
        self.assertEqual(golden_render, rendered)

    def test_read_file(self):
        item = {
            "type": "TEXT",
            "origin": "test_read.md"
        }

        golden_text = "multi\nline\n"""

        self.assertEqual(golden_text, list(PP.read_file([item]))[0]["content_raw"])
        self.assertEqual(golden_text, list(PP.read_file([item]))[0]["output"])

        with self.assertRaises(FileNotFoundError) as context:
            item["origin"] = "abc"
            list(PP.read_file([item]))
        self.assertTrue("No file at specified origin." in str(context.exception))

        with self.assertRaises(FileNotFoundError) as context:
            list(PP.read_file([self.item]))
        self.assertTrue("No file at specified origin." in str(context.exception))

    def test_write_file(self):
        def readf(item):
            with open(item["destination"], "r") as f:
                return f.read()

        test_item = {
            "destination": "new/new.txt",
            "output": "multi\nline",
            "action": "",
            "origin": ""
        }

        PP.write_file([test_item])
        self.assertEqual(test_item["output"], readf(test_item))

        PP.write_file([test_item])
        self.assertEqual(test_item["output"], readf(test_item))

        test_item_ext = {
            "destination": "new/new.txt",
            "output": "multi\nline",
            "action": "",
            "origin": "",
            "meta": {
                "extension": "md"
            }
        }

        test_item_ext_gold = {
            "destination": "new/new.md"
        }

        PP.write_file([test_item_ext])
        self.assertEqual(test_item["output"], readf(test_item_ext_gold))

        test_item_no_render = test_item_ext | {
            "meta": {
                "no_render": True
            },
            "destination": "no_render.txt"
        }

        PP.write_file([test_item_no_render])
        self.assertFalse(os.path.exists("no_render.txt"))

    def test_load_image(self):
        item = self.item | {
            "origin": "test_load.png"
        }

        test_image = list(PP.load_image([item]))[0]["image"]
        self.assertTrue(isinstance(test_image, PngImageFile))

        with self.assertRaises(UnidentifiedImageError) as context:
            item = self.item | {
                "origin": "test_read.md"
            }
            print(list(PP.load_image([item])))
        self.assertTrue("Specified file is not an image." in str(context.exception))

        with self.assertRaises(FileNotFoundError) as context:
            list(PP.load_image([self.item]))
        self.assertTrue("No image at specified origin." in str(context.exception))

    def test_save_image(self):
        def loadi(item):
            return Image.open(item["destination"])

        test_item = {
            "destination": "new/new.png",
            "image": Image.open("test_load.png"),
            "action": "",
            "origin": "",
            "extension": "png"
        }

        PP.save_image([test_item])
        first = loadi(test_item)
        self.assertFalse(ImageChops.difference(test_item["image"], first).getbbox())

        test_item["image"] = Image.open("test_save.png")
        test_item["quality"] = 100
        PP.save_image([test_item])
        second = loadi(test_item)
        self.assertFalse(ImageChops.difference(test_item["image"], second).getbbox())

        self.assertNotEqual(first.size, second.size)

        with patch("barely.core.ProcessingPipeline.copy_file") as copy_file:
            test_item["copymode"] = True
            PP.save_image([test_item])
            self.assertTrue(copy_file.called)

    def test_copy_file(self):
        def readf(item, key):
            with open(item[key], "r") as f:
                return f.read()

        test_item = {
            "origin": "test_read.md",
            "destination": "copy/file.md",
            "action": ""
        }

        PP.copy_file([test_item])
        self.assertEqual(readf(test_item, "origin"), readf(test_item, "destination"))

        PP.copy_file([test_item])
        self.assertEqual(readf(test_item, "origin"), readf(test_item, "destination"))

    def test_delete(self):
        os.chdir("delete")
        PP.delete("dir")
        PP.delete("nothere")
        PP.delete("file.txt")
        self.assertFalse(os.path.exists("dir"))
        self.assertFalse(os.path.exists("file.txt"))
        os.chdir("..")

    def test_move(self):
        def readf(path):
            with open(path, "r") as file:
                return file.read()

        os.chdir("move")

        PP.move("fro.txt", "moved.txt")
        self.assertTrue(os.path.isfile("moved.txt"))
        first = readf("moved.txt")

        PP.move("fro2.txt", "moved.txt")
        self.assertTrue(os.path.isfile("moved.txt"))
        second = readf("moved.txt")

        self.assertNotEqual(first, second)

        PP.move("fro", "to")
        self.assertTrue(os.path.isdir("to"))
        self.assertTrue(os.path.isfile(os.path.join("to", "collateral")))

        PP.move("fro2", "to")
        self.assertTrue(os.path.isdir("to"))
        self.assertTrue(os.path.isfile(os.path.join("to", "collateral")))

        self.assertFalse(os.path.exists("fro"))
        self.assertFalse(os.path.exists("fro.txt"))
        self.assertFalse(os.path.exists("fro2.txt"))

        os.chdir("..")

    def test_extract_template(self):
        item = {
            "origin": "template.md"
        }
        self.assertEqual("template.html", list(PP.extract_template([item]))[0]["template"])

        item["origin"] = "template.subtemplate.md"
        self.assertEqual(os.path.join("template", "subtemplate.html"), list(PP.extract_template([item]))[0]["template"])

    def test_parse_meta(self):
        def get_yaml(file):
            with open(file, "r") as f:
                item = {
                    "content_raw": f.read()
                }
                return list(PP.parse_meta([item]))[0]["meta"]

        os.chdir("content_files")
        golden_dict = {
            "value": "a"
        }

        self.assertDictEqual({}, get_yaml("EMPTY.md"))
        self.assertDictEqual({}, get_yaml("ONLY_MD.md"))
        self.assertDictEqual(golden_dict, get_yaml("ONLY_YAML.md"))
        self.assertDictEqual(golden_dict, get_yaml("MULTI_YAML.md"))
        open("metadata.yaml", 'a')  # just for the test coverage...
        self.assertDictEqual(golden_dict, get_yaml("ONE_YAML_ONE_MD.md"))

        os.chdir("..")

    def test_parse_content(self):
        def get_content(file):
            with open(file, "r") as f:
                item = {
                    "content_raw": f.read()
                }
                return list(PP.parse_content([item]))[0]["content"]

        os.chdir("content_files")
        golden_html = "<h1>Title</h1>\n"

        self.assertEqual("", get_content("EMPTY.md"))
        self.assertEqual("", get_content("ONLY_YAML.md"))
        self.assertEqual(golden_html, get_content("ONLY_MD.md"))
        self.assertEqual(golden_html, get_content("ONE_YAML_ONE_MD.md"))
        self.assertEqual("<h2>value2: b</h2>\n" + golden_html, get_content("MULTI_YAML.md"))

        os.chdir("..")

    def test_handle_subpages(self):
        parent = {
            "origin": "subpages/parent.md",
            "meta": {
                "modular": ["subpage"]
            }
        }
        with patch("barely.core.ProcessingPipeline.pipe_subpage") as pipe_subpage:
            list(PP.handle_subpages([parent]))
            self.assertTrue(pipe_subpage.called)

        parent["meta"] = {}
        with patch("barely.core.ProcessingPipeline.pipe_subpage") as pipe_subpage:
            list(PP.handle_subpages([parent]))
            self.assertFalse(pipe_subpage.called)

    def test_render_page(self):
        def get_output(template, content=""):
            item = {
                "template": template,
                "content": content,
                "meta": {}
            }
            return list(PP.render_page([item]))[0]["output"]

        self.assertEqual("test", get_output("template.html", "test"))
        self.assertEqual("", get_output("template.html"))

        PP.render_page([{
            "template": "",
            "content": "",
            "meta": {}
            }])

    def test_hook_plugins(self):
        hooked = list(PP.hook_plugins([{"test": "a"}]))[0]
        self.assertTrue(PP.PM.hook_content.called)
        self.assertDictEqual({"test": "a"}, hooked)
