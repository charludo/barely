import unittest


loader = unittest.TestLoader()
startdir = "/home/charlotte/Webdesign/barely/barely/tests"
suite = loader.discover(startdir)

runner = unittest.TextTestRunner()
runner.run(suite)
