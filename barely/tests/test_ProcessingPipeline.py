import os
import unittest
from mock import patch
from PIL.PngImagePlugin import PngImageFile
from PIL import Image, ImageChops, UnidentifiedImageError
import barely.core.ProcessingPipeline as PP


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

    @classmethod
    def tearDownClass(self):
        os.chdir("..")

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
        pass

    def test_pipe_image(self):
        pass

    def test_pipe_text(self):
        pass

    def test_pipe_generic(self):
        pass

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
            "output": "multi\nline"
        }

        PP.write_file([test_item])
        self.assertEqual(test_item["output"], readf(test_item))

        PP.write_file([test_item])
        self.assertEqual(test_item["output"], readf(test_item))

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
            "image": Image.open("test_load.png")
        }

        PP.save_image([test_item])
        first = loadi(test_item)
        self.assertFalse(ImageChops.difference(test_item["image"], first).getbbox())

        test_item["image"] = Image.open("test_save.png")
        PP.save_image([test_item])
        second = loadi(test_item)
        self.assertFalse(ImageChops.difference(test_item["image"], second).getbbox())

        self.assertNotEqual(first.size, second.size)

    def test_copy_file(self):
        def readf(item, key):
            with open(item[key], "r") as f:
                return f.read()

        test_item = {
            "origin": "test_read.md",
            "destination": "copy/file.md"
        }

        PP.copy_file([test_item])
        self.assertEqual(readf(test_item, "origin"), readf(test_item, "destination"))

        PP.copy_file([test_item])
        self.assertEqual(readf(test_item, "origin"), readf(test_item, "destination"))

        with self.assertRaises(FileNotFoundError) as context:
            list(PP.copy_file([self.item]))
        self.assertTrue("No file at specified origin." in str(context.exception))

    def test_extract_template(self):
        item = {
            "origin": "template.md"
        }
        self.assertEqual("template.html", list(PP.extract_template([item]))[0]["template"])

        item["origin"] = "template.subtemplate.md"
        self.assertEqual("template/subtemplate.html", list(PP.extract_template([item]))[0]["template"])

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
        self.assertDictEqual(golden_dict, get_yaml("ONE_YAML_ONE_MD.md"))

        os.chdir("..")

    def test_parse_content(self):
        pass

    def test_handle_subpages(self):
        pass

    def test_render_page(self):
        pass

    def test_hook_plugins(self):
        pass
