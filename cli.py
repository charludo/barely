"""
functions that are available to be called
from the cli by the user.
"""
import os
import sys


def init():
    # TEMPORARY
    os.chdir("blueprints/devroot")

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
    os.chdir("../..")


def track():
    from multiprocessing import Process
    from livereload import Server
    from barely.common.config import config
    from barely.core.ChangeTracker import ChangeTracker
    from barely.core.EventHandler import EventHandler

    EH = EventHandler()
    EH.init_pipeline()

    CT = ChangeTracker()
    CT.register_handler(EH.notify)

    server = Server()
    server.watch(config["ROOT"]["DEV"], delay=0, open_url_delay=0)

    tracking_process = Process(name="barely_tracker", target=CT.start)
    serving_process = Process(name="live_server", target=server.serve)

    tracking_process.track()
    serving_process.start()


def test():
    # import coverage
    import unittest
    import shutil

    # TEMPORARY
    testdir = "/home/charlotte/test_barely"

    testsuite_dir = os.path.join(os.getcwd(), "barely", "tests")
    shutil.copytree(os.path.join(testsuite_dir, "ressources"), testdir)

    os.chdir(testdir)
    os.environ["barely"] = os.getcwd()

    loader = unittest.TestLoader()
    suite = loader.discover(testsuite_dir)

    # cov = coverage.Coverage()
    # cov.start()

    runner = unittest.TextTestRunner()
    runner.run(suite)

    # cov.stop()
    # cov.save()
    # cov.html_report()

    shutil.rmtree(testdir)


if __name__ == "__main__":
    init()
    test()
