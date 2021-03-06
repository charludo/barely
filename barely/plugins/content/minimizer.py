"""
Minimizer exports the singleton Minimzer,
which in turn provides functons to minimize
images, javascript,...
It also functions as a sass/scss parser.
"""
import sass
from PIL import Image
from calmjs.parse import es5
from calmjs.parse.unparsers.es5 import minify_print
from .filereader import FileReader
from barely.common.config import config
from barely.common.utils import write_file, get_extension
from barely.common.decorators import Singleton


@Singleton
class Minimizer(object):
    """ Minimizer provides functions to reduce various formats in size """

    def __init__(self):
        self.fr = FileReader()

    def minimize(self, dev, web):
        extension = get_extension(dev)
        if extension in config["FILETYPES"]["COMPRESSABLE"]["CSS"]:
            self.minimize_css(dev, web)
        elif extension in config["FILETYPES"]["COMPRESSABLE"]["JS"]:
            self.minimize_js(dev, web)
        elif extension in config["FILETYPES"]["COMPRESSABLE"]["IMAGES"]:
            self.minimize_image(dev, web)
        else:
            raise f"Cant minimize {dev} - no minimizer rovided for the extension {extension}"

    def minimize_css(self, dev, web):
        compiled = sass.compile(filename=dev, output_style="compressed")  # 1. compile to css and compress
        write_file(web, compiled)                                         # 2. write & done!

    def minimize_js(self, dev, web):
        raw = self.fr.get_raw(dev)
        minified = minify_print(es5(raw), obfuscate=True, obfuscate_globals=True)  # 1. minify & mangle
        write_file(web, minified)                                                  # 2. write & done!

    def minimize_image(self, dev, web):
        quality = int(config["IMAGES"]["QUALITY"])                  # load parameter
        short_side = int(config["IMAGES"]["LONG_SIDE"])
        size = short_side, short_side                               # apply based on orientation

        with Image.open(dev) as original:
            original.thumbnail(size, Image.ANTIALIAS)               # doesn't care about orientation
            original.save(web, optimize=True, quality=quality)      # should make a nice small size!
