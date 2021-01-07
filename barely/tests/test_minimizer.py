import os
import unittest
from PIL import Image
from barely.render import MINIMIZER as MIN
from ref.utils import read, write, remove, testdir
from barely.common.config import config


class TestRenderer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.mindir = os.path.join(testdir, "minimizer")

    def test_minimize_css(self):
        original_path = os.path.join(self.mindir, "file.sass")
        mini_path = os.path.join(self.mindir, "mini.min.css")
        MIN.minimize_css(original_path, mini_path)

        self.assertTrue(os.path.isfile(mini_path))

        original_size = os.stat(original_path).st_size
        mini_size = os.stat(mini_path).st_size

        self.assertLess(mini_size, original_size)
        self.assertEqual(read(os.path.join("minimizer", "mini.min.css")), ".alert{border:1px solid rgba(198,83,140,0.88)}\n")

        remove(mini_path)

    def test_minimize_js(self):
        original_path = os.path.join(self.mindir, "file.js")
        mini_path = os.path.join(self.mindir, "mini.min.js")
        MIN.minimize_js(original_path, mini_path)

        self.assertTrue(os.path.isfile(mini_path))

        original_size = os.stat(original_path).st_size
        mini_size = os.stat(mini_path).st_size

        self.assertLess(mini_size, original_size)
        self.assertEqual(read(os.path.join("minimizer", "mini.min.js")), "function a(a){var b=a*a;return b;}var b=a(4);alert(square);")

        remove(mini_path)

    def test_minimize_image(self):
        original_path = os.path.join(self.mindir, "image.jpg")
        mini_path = os.path.join(self.mindir, "mini.jpg")
        MIN.minimize_image(original_path, mini_path)

        self.assertTrue(os.path.isfile(mini_path))

        original_size = os.stat(original_path).st_size
        mini_size = os.stat(mini_path).st_size

        self.assertLess(mini_size, original_size)

        original_image = Image.open(original_path)
        o_width, o_height = original_image.size
        o_short = o_width if o_width < o_height else o_height

        mini_image = Image.open(mini_path)
        m_width, m_height = mini_image.size
        m_short = m_width if m_width < m_height else m_height
        m_long = m_width if m_width > m_height else m_height

        self.assertEqual(m_long, int(config["IMAGES"]["LONG_SIDE"]))
        self.assertLess(m_short, o_short)

        remove(mini_path)
