import re
import unittest
from mock import patch
from barely.plugins.content.Highlight.highlight import Highlight


class TestHighlight(unittest.TestCase):

    maxDiff = None

    def test___init__(self):
        golden = {
            "PRIORITY": 20,
            "CLASS_PREFIX": "hl",
            "LINE_NOS": "table",
            "TABSIZE": 4,
            "ENCODING": "utf-8",
            "THEME": "default",
            "LEXER": "",
            "ASSETS_DIR": "assets"
        }

        hl = Highlight()
        self.assertDictEqual(golden, hl.plugin_config)

        hl.config["HIGHLIGHT"] = {"PRIORITY": -1}
        hl.__init__()

        golden["PRIORITY"] = -1
        self.assertDictEqual(golden, hl.plugin_config)

        # reset
        del hl.config["HIGHLIGHT"]
        hl.__init__()

    def test_register(self):
        hl = Highlight()
        name, prio, ext = hl.register()

        self.assertEqual(name, "Highlight")
        self.assertEqual(prio, 20)
        self.assertEqual(ext, ["md"])

    @patch("barely.plugins.content.Highlight.highlight.write_file")
    def test_action(self, write_file):
        item = {
            "action": "rendered",
            "content": """
            <pre><code>
                def test_register(self):
                hl = Highlight()
                name, prio, ext = hl.register()

                self.assertEqual(name, "Highlight")
                self.assertEqual(prio, 20)
                self.assertEqual(ext, ["md"])</code></pre>
            """
        }

        golden_hl = """
        <hl><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre><span class="normal">1</span>\n<span class="normal">2</span>\n<span
        class="normal">3</span>\n<span class="normal">4</span>\n<span class="normal">5</span>\n<span class="normal">6</span>\n<span class="normal">7</span>
        </pre></div></td><td class="code"><div class="highlight"><pre><span></span><span class="hlk">def</span> <span class="hlnf">test_register</span><span
        class="hlp">(</span><span class="hlbp">self</span><span class="hlp">):</span>\n        <span class="hln">hl</span> <span class="hlo">=</span>
        <span class="hln">Highlight</span><span class="hlp">()</span>\n        <span class="hln">name</span><span class="hlp">,</span> <span class="hln">prio
        </span><span class="hlp">,</span> <span class="hln">ext</span> <span class="hlo">=</span> <span class="hln">hl</span><span class="hlo">.</span>
        <span class="hln">register</span><span class="hlp">()</span>\n\n        <span class="hlbp">self</span><span class="hlo">.</span><span class="hln">
        assertEqual</span><span class="hlp">(</span><span class="hln">name</span><span class="hlp">,</span> <span class="hls2">&quot;Highlight&quot;</span><span
        class="hlp">)</span>\n        <span class="hlbp">self</span><span class="hlo">.</span><span class="hln">assertEqual</span><span class="hlp">(</span>
        <span class="hln">prio</span><span class="hlp">,</span> <span class="hlmi">20</span><span class="hlp">)</span>\n        <span class="hlbp">self</span>
        <span class="hlo">.</span><span class="hln">assertEqual</span><span class="hlp">(</span><span class="hln">ext</span><span class="hlp">,</span>
        <span class="hlp">[</span><span class="hls2">&quot;md&quot;</span><span class="hlp">])</span>\n</pre></div>\n</td></tr></table></hl>
        """

        hl = Highlight()
        hl.plugin_config["LEXER"] = "python"

        result = list(hl.action(item=item.copy()))[0]

        self.assertEqual(re.sub(r'[\s+]', '', golden_hl), re.sub(r'[\s+]', '', result["content"]))
        self.assertEqual("rendered, highlighted", result["action"])
        self.assertListEqual(["/assets/highlight/default.css"], result["additional_styles"])
        self.assertTrue(write_file.called)

        write_file.reset_mock()

        item = {
            "action": "rendered",
            "content": """
            <pre><code class="language-rust">
            fn main() {
                println!("Hello World!");
            }</code></pre>
            """,
            "meta": {
                "highlight": {
                    "THEME": "pastie"
                }
            }
        }

        golden_hl = """
        <hl><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre><span class="normal">1</span>\n<span class="normal">2</span>\n
        <span class="normal">3</span></pre></div></td><td class="code"><div class="highlight"><pre><span></span><spanclass="hlw"></span><span class="hlk">fn</span> <span class="hlnf">
        main</span><span class="hlp">()</span><span class="hlw"> </span><span class="hlp">{</span><span class="hlw"></span>\n<span class="hlw">
        </span><span class="hlfm">println!</span><span class="hlp">(</span><span class="hls">&quot;Hello World!&quot;</span><span class="hlp">);</span>
        <span class="hlw"></span>\n<span class="hlw">            </span><span class="hlp">}</span><span class="hlw"></span>\n</pre></div>\n</td></tr></table></hl>
        """

        result = list(hl.action(item=item.copy()))[0]

        self.assertEqual(re.sub(r'[\s+]', '', golden_hl), re.sub(r'[\s+]', '', result["content"]))
        self.assertEqual("rendered, highlighted", result["action"])
        self.assertListEqual(["/assets/highlight/pastie.css"], result["additional_styles"])
        self.assertTrue(write_file.called)
