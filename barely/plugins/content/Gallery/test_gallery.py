import re
import os
import unittest
from barely.plugins.content.Gallery.gallery import Gallery


class TestGallery(unittest.TestCase):

    def test_action(self):
        img_path = os.path.join("Plugins", "Gallery")
        item = {
            "content": f"[examplegallery name desc]!!({img_path})"
        }

        golden = """
        <div class="gallery" id="gallery-examplegallery">
        <img src="Plugins/Gallery/c.png" alt="image 1 in examplegallery gallery">
        <img src="Plugins/Gallery/b.jpg" alt="image 2 in examplegallery gallery">
        <img src="Plugins/Gallery/a.png" alt="image 3 in examplegallery gallery">
        </div>
        """

        g = Gallery()
        result = list(g.action(item=item))[0]["content"]
        self.assertEqual(re.sub(r'[\s+]', '', result), re.sub(r'[\s+]', '', golden))
