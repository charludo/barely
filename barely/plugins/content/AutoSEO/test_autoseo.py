import re
import os
import unittest
from barely.plugins.content.AutoSEO.autoseo import AutoSEO


class TestAutoSEO(unittest.TestCase):

    maxDiff = None

    def test_action(self):
        global_meta = {
            "site_url": "https://test.com",
            "site_name": "Test Site",
            "site_description": "Description of test site",
            "site_keywords": ["one"],
            "favicon": "favicon.ico"
        }

        page_meta = {
            "title": "Test Page",
            "summary": "just a simple page for testing",
            "SEO": {
                "description": "AMAZING TEST PAGE!!"
            }
        }

        content = """
            <p><img alt="Test Image One" src="first.png"></p>
            <p><img alt="Test Image Two" src="second.png" /></p>
        """

        item = {
            "content": content,
            "meta": global_meta | page_meta,
            "destination": "web/subpage/index.html"
        }

        golden_tags = """
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Test Page | Test Site</title>
            <meta name="description" content="just a simple page for testing" />
            <meta name="keywords" content="one" />
            <meta name="robots" content="all" />
            <link rel="shortcut icon" type="image/x-icon" href="favicon.ico">
            <meta property="og:title" content="Test Page">
            <meta property="og:description" content="AMAZING TEST PAGE!!">
            <meta property="og:image" content="https://test.com/subpage/first.png">
            <meta property="og:url" content="https://test.com/subpage/index.html">
            <meta property="og:site_name" content="Test Site">
            <meta name="twitter:image:alt" content="AMAZING TEST PAGE!!">
            <meta name="twitter:card" content="summary_card_large">
        """

        aseo = AutoSEO()
        result = list(aseo.action(item=item))[0]["meta"]["seo_tags"]
        self.assertEqual(re.sub(r'[\s+]', '', result), re.sub(r'[\s+]', '', golden_tags))

    def test__first_image(self):
        aseo = AutoSEO()
        result = aseo._first_image(os.path.join("Plugins", "AutoSEO"))
        self.assertDictEqual(result, {
            "og:image": "Plugins/AutoSEO/b.jpg"
        })
