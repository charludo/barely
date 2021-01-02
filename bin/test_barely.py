import unittest


loader = unittest.TestLoader()
startdir = "/home/charlotte/Webdesign/cms/barely/test"
suite = loader.discover(startdir)

runner = unittest.TextTestRunner()
runner.run(suite)
