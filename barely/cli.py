"""
functions that are available to be called
from the cli by the user.
"""
import os
import sys
import click


def init():
    cwd = os.getcwd()

    # try to find the config.yaml
    if os.path.exists("config.yaml"):
        # export the cwd as an environment variable
        os.environ["barely"] = cwd
    else:
        print("barely :: could not find 'config.yaml'. Exiting")
        sys.exit()


@click.group()
def run():
    pass


@run.command()
def track():
    init()

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


@run.command()
def rebuild():
    init()

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


@run.command()
def test():
    # import coverage
    import unittest
    import shutil

    # TEMPORARY
    testdir = "/home/charlotte/.barely/ACTIVETEST"

    testsuite_dir = os.path.join(os.path.dirname(__file__), "tests")
    shutil.copytree(os.path.join(testsuite_dir, "ressources"), testdir)

    os.chdir(testdir)
    os.environ["barely"] = testdir

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


if __name__ == "__main__":
    os.chdir("blueprints/devroot")
    init()
    os.chdir("../..")
    test()
