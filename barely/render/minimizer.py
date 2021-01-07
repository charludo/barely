"""
Minimizer exports the singleton Minimzer,
which in turn provides functons to minimize
images, javascript,...
It also functions as a sass/scss parser.
"""
import sass
import csscompressor
import slimit
from PIL import Image
from .filereader import FileReader
from barely.common.config import config
from barely.common.utils import write_file
from barely.common.decorators import Singleton


@Singleton
class Minimizer(object):
    """ Minimizer provides functions to reduce various formats in size """

    def __init__(self):
        self.fr = FileReader()

    def minimize_css(self, dev, web):
        uncompiled = self.fr.get_raw(dev)               # super easy:
        compiled = sass.compile(uncompiled)             # 1. compile to css
        compressed = csscompressor.compress(compiled)   # 2. compress that css
        write_file(web, compressed)                     # 3. write & done!

    def minimize_js(self, dev, web):
        raw = self.fr.get_raw(dev)                                          # even easier:
        minified = slimit.minify(raw, mangle=True, mangle_toplevel=True)    # 1. minify & mangle
        write_file(web, minified)                                           # 2. write & done!

    def minimize_images(self, dev, web):
        quality = config["IMAGES"]["QUALITY"]                       # load parameter
        short_side = config["IMAGES"]["SHORT_SIDE"]
        size = short_side, short_side                               # apply based on orientation

        with Image.open(dev) as original:
            original.thumbnail(size, Image.ANTIALIAS)               # doesn't care about orientation
            original.save(web, optimize=True, quality=quality)      # should make a nice small size!
