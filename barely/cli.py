"""
functions that are available to be called
from the cli by the user.
"""
import os
import sys
import argparse


def init():
    cwd = os.getcwd()

    # try to find the config.yaml
    if os.path.exists("config.yaml"):
        # export the cwd as an environment variable
        os.environ["barely"] = cwd
    else:
        print("barely :: could not find 'config.yaml'. Exiting")
        sys.exit()


def track():
    from barely.core.EventHandler import EventHandler
    from barely.core.ChangeTracker import ChangeTracker
    from barely.plugins.PluginManager import PluginManager

    PM = PluginManager()
    EH = EventHandler()
    EH.init_pipeline(PM)

    CT = ChangeTracker()
    CT.register_handler(EH)

    CT.track()
    aftermath(PM)


def rebuild():
    from barely.core.EventHandler import EventHandler
    from barely.plugins.PluginManager import PluginManager

    PM = PluginManager()
    EH = EventHandler()
    EH.init_pipeline(PM)

    EH.force_rebuild()
    aftermath(PM)


def aftermath(PM):
    print("barely ..")
    print("barely :: Do you want to Publish / Backup / do both?")
    action = input("       -> [n]othing | [p]ublish | [b]ackup | *[Y]do both :: ").lower()

    if action.startswith("p") or action.startswith("y") or action == "":
        print("barely :: publishing...")
        PM.hook_publication()
        print("       -> ...done.")
    if action.startswith("b") or action.startswith("y") or action == "":
        print("barely :: backuping...")
        PM.hook_backup()
        print("       -> ...done.")

    print("barely :: exited.")


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

    runner = unittest.TextTestRunner(buffer=True)
    runner.run(suite)

    # cov.stop()
    # cov.save()
    # cov.html_report()

    shutil.rmtree(testdir)


def run():
    parser = argparse.ArgumentParser()
    FUNCTION_MAP = {
        "test": test,
        "build": rebuild,
        "track": track
    }

    parser.add_argument("command",
                        nargs="?",
                        default="track",
                        help="command which barely should execute",
                        choices=FUNCTION_MAP.keys())
    args = parser.parse_args()

    command = FUNCTION_MAP[args.command]

    init()
    command()


if __name__ == "__main__":
    os.chdir("blueprints/devroot")
    init()
    os.chdir("../..")

    test()
