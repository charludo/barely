import re
import unittest
from barely.plugins.content.ToC.toc import ToC


class TestToC(unittest.TestCase):

    def test___init__(self):
        golden = {
            "PRIORITY": 2,
            "MIN_DEPTH": 1,
            "MAX_DEPTH": 4,
            "LIST_ELEMENT": "ul"
        }

        toc = ToC()
        self.assertDictEqual(golden, toc.plugin_config)

        toc.config["TOC"] = {"PRIORITY": 12}
        toc.__init__()
        golden["PRIORITY"] = 12

        self.assertDictEqual(golden, toc.plugin_config)

        # reset
        del toc.config["TOC"]
        toc.__init__()

    def test_register(self):
        toc = ToC()
        name, prio, ext = toc.register()

        self.assertEqual(name, "ToC")
        self.assertEqual(prio, 2)
        self.assertEqual(ext, ["md"])

    def test_action(self):
        item = {
            "content": """
                <html>
                <head>
                </head>
                <body>
                <h2>A 2</h2>
                <p></p>
                <h2>B 2</h2>
                <p></p>
                <h3>C 3</h3>
                <p></p>
                <h2>D 2</h2>
                <p></p>
                <h3>E 3</h3>
                <p></p>
                <h4>F 4</h4>
                <p></p>
                <h4>G 4</h4>
                <p></p>
                <h3>H 3</h3>
                <p></p>
                </body>
                </html>
            """,
            "meta": {}
        }

        golden = {
            "content": """
                <html>
                <head>
                </head>
                <body>
                <h2 id="a-2">A 2</h2>
                <p></p>
                <h2 id="b-2">B 2</h2>
                <p></p>
                <h3 id="c-3">C 3</h3>
                <p></p>
                <h2 id="d-2">D 2</h2>
                <p></p>
                <h3 id="e-3">E 3</h3>
                <p></p>
                <h4 id="f-4">F 4</h4>
                <p></p>
                <h4 id="g-4">G 4</h4>
                <p></p>
                <h3 id="h-3">H 3</h3>
                <p></p>
                </body>
                </html>
            """,
            "meta": {
                "toc": """
                <div class="toc">
                <ul>
                <ul>
                <li><a href="#a-2">A 2</a></li>
                <li><a href="#b-2">B 2</a></li>
                <ul>
                <li><a href="#c-3">C 3</a></li>
                </ul>
                <li><a href="#d-2">D 2</a></li>
                <ul>
                <li><a href="#e-3">E 3</a></li>
                <ul>
                <li><a href="#f-4">F 4</a></li>
                <li><a href="#g-4">G 4</a></li>
                </ul>
                <li><a href="#h-3">H 3</a></li>
                </ul>
                </ul>
                </ul>
                </div>
                """
            }
        }

        toc = ToC()
        result = list(toc.action(item=item))
        self.assertEqual(1, len(result))

        self.assertEqual(item["content"], golden["content"])
        self.assertEqual(re.sub(r'[\s+]', '', item["meta"]["toc"]), re.sub(r'[\s+]', '', golden["meta"]["toc"]))
