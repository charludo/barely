"""
Minify provides functons to minimize
javascript. It also functions
as a sass/scss parser.
"""
import os
import sass
from calmjs.parse import es5, exceptions as js_exceptions
from calmjs.parse.unparsers.es5 import minify_print
from barely.plugins import PluginBase


class Minify(PluginBase):
    # Minify provides functions to compile and reduce scss and js in size

    def __init__(self):
        super().__init__()

        standard_config = {
            "PRIORITY": 3,
            "JS_OBFUSCATE": True,
            "JS_OBFUSCATE_GLOBALS": True,
            "CSS_INCLUDE_COMMENTS": False,
            "CSS_OUTPUT_STYLE": "compressed"
        }
        try:
            self.plugin_config = standard_config | self.config["MINIFY"]
        except KeyError:
            self.plugin_config = standard_config
            self.func_map = {
                "js": self.minimize_js,
                "sass,scss": self.minimize_css
            }
            self.register_for = sum([group.split(",") for group in self.func_map.keys()], [])

    def register(self):
        return "Minify", self.plugin_config["PRIORITY"], self.register_for

    def action(self, *args, **kwargs):
        if "item" in kwargs:
            item = kwargs["item"]
            for key, func in self.func_map.items():
                if item["extension"] in key:
                    yield func(item)

    def minimize_css(self, item):
        try:
            indented = True if item["extension"] == "sass" else False
            compiled = sass.compile(string=item["content_raw"], output_style=self.plugin_config["CSS_OUTPUT_STYLE"],
                                    indented=indented, source_comments=self.plugin_config["CSS_INCLUDE_COMMENTS"])
            item["destination"] = os.path.splitext(item["destination"])[0] + ".css"
            item["action"] = "compiled"
            item["output"] = compiled
        except sass.CompileError as e:
            self.logger.error(f"SASS Compile {e}")
        return item

    def minimize_js(self, item):
        try:
            minified = minify_print(es5(item["output"]), obfuscate=self.plugin_config["JS_OBFUSCATE"],
                                    obfuscate_globals=self.plugin_config["JS_OBFUSCATE_GLOBALS"])
            item["output"] = minified
            item["action"] = "compiled"
        except js_exceptions.ECMASyntaxError as e:
            self.logger.error(f"JS Syntax Error: {e}")
        return item
