import os
import unittest
from mock import patch
import barely.core.ProcessingPipeline as PP


class TestProcessingPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        os.chdir("ProcessingPipeline")

    @classmethod
    def tearDownClass(self):
        os.chdir("..")

    def test_process(self):
        with patch("barely.core.ProcessingPipeline.pipe_page") as pipe_page:
            item = {
                "type": "PAGE"
            }
            PP.process([item])
            self.assertTrue(pipe_page.called)

        with patch("barely.core.ProcessingPipeline.pipe_image") as pipe_image:
            item = {
                "type": "IMAGE"
            }
            PP.process([item])
            self.assertTrue(pipe_image.called)

        with patch("barely.core.ProcessingPipeline.pipe_text") as pipe_text:
            item = {
                "type": "TEXT"
            }
            PP.process([item])
            self.assertTrue(pipe_text.called)

        with patch("barely.core.ProcessingPipeline.pipe_generic") as pipe_generic:
            item = {
                "type": "GENERIC"
            }
            PP.process([item])
            self.assertTrue(pipe_generic.called)

        self.assertRaises(TypeError, PP.process, 0)
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
        pass

    def test_write_file(self):
        pass

    def test_load_image(self):
        pass

    def test_save_image(self):
        pass

    def test_copy_file(self):
        pass

    def test_extract_template(self):
        pass

    def test_parse_meta(self):
        pass

    def test_parse_content(self):
        pass

    def test_handle_subpages(self):
        pass

    def test_render_page(self):
        pass

    def test_hook_plugins(self):
        pass
