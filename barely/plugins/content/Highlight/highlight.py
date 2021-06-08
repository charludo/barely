"""
highlight <code> blocks with pygments
"""
import re
import os
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_by_name
from barely.plugins import PluginBase
from barely.core.ProcessingPipeline import write_file


class Highlight(PluginBase):
    # make js-highlighting unnecessary by providing hightlighted pure html/css code blocks

    def __init__(self):
        super().__init__()
        standard_config = {
            "PRIORITY": 20,
            "CLASS_PREFIX": "hl",
            "LINE_NOS": "table",
            "TABSIZE": 4,
            "ENCODING": "utf-8",
            "THEME": "default",
            "LEXER": "",
            "ASSETS_DIR": "assets"
            }
        try:
            self.plugin_config = standard_config | self.config["HIGHLIGHT"]
        except KeyError:
            self.plugin_config = standard_config

    def register(self):
        return "Highlight", self.plugin_config["PRIORITY"], [self.config["PAGE_EXT"]]

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]
            self.additional_styles = set()

            # accept page-level config for this plugin
            try:
                self.page_config = self.plugin_config | item["meta"]["highlight"]
            except KeyError:
                self.page_config = self.plugin_config.copy()

            item["content"] = re.sub(r"<pre><code>(.*)</code></pre>", self._handle_code, item["content"], flags=re.S)
            item["action"] = "rendered, highlighted"
            item["additional_styles"] = list(self.additional_styles)
            yield item

    def _handle_code(self, match):
        code = match.group(1)

        # if no lexer is set anywhere: guess it
        lexer_args = {
            "tabsize": self.page_config["TABSIZE"],
            "encoding": self.page_config["ENCODING"]
        }
        lexer = guess_lexer(code, **lexer_args)

        # use global (or page-level!) config lexer, if set
        try:
            lexer = get_lexer_by_name(self.page_config["LEXER"], **lexer_args)
        except Exception:
            pass

        # "best case": lexer is set right in the code snippet; obviously use it
        try:
            matches = re.search(r"\[lexer:\s*(.+)\]$[\s]*([\s\S]*)", code, re.MULTILINE)
            lexer_name = matches.group(1)
            code = matches.group(2)
            lexer = get_lexer_by_name(lexer_name, **lexer_args)
        except Exception:
            pass

        formatter_args = {
            "classprefix": self.page_config["CLASS_PREFIX"],
            "linenos": self.page_config["LINE_NOS"],
            "style": self.page_config["THEME"]
        }
        formatter = HtmlFormatter(**formatter_args)

        css = formatter.get_style_defs(self.page_config["CLASS_PREFIX"])
        css_path = os.path.join(self.config["ROOT"]["DEV"], self.page_config["ASSETS_DIR"], "highlight", self.page_config["THEME"]) + ".css"
        self.additional_styles.add(f"/{self.page_config['ASSETS_DIR']}/highlight/{self.page_config['THEME']}.css")
        write_file([
            {
                "destination": css_path,
                "origin": f"Code Hightlight Style: {self.page_config['THEME']}",
                "action": "generated styles",
                "output": css
            }
        ])

        return highlight(code, lexer, formatter)
