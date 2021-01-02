"""
functions that are available to be called
from the cli by the user.
"""
import os
import sys


def init():
    # TEMPORARY
    os.chdir("blueprints")

    # get dir from which barely was started
    cwd = os.getcwd()

    # try to find the config.yaml
    if os.path.exists("config.yaml"):
        # export the cwd as an environment variable
        os.environ["barely"] = cwd
    else:
        print("barely :: could not find 'config.yaml'. Exiting")
        sys.exit()

    # TEMPORARY
    os.chdir("..")


def test():
    import unittest

    loader = unittest.TestLoader()
    startdir = os.path.join(os.getcwd(), "barely", "tests")
    suite = loader.discover(startdir)

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    init()
    test()
