"""
functions that are available to be called
from the cli by the user.
"""


def test():
    import unittest
    import os

    loader = unittest.TestLoader()
    startdir = os.path.join(os.getcwd(), "barely", "tests")
    suite = loader.discover(startdir)

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    test()
