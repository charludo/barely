"""
functions that are available to be called
from the cli by the user.
"""
import os
import sys
import click
import platform
from pathlib import Path


def init():
    # try to find the config.yaml
    if os.path.exists("config.yaml"):
        # export the cwd as an environment variable
        appdir = get_appdir()
        os.environ["barely"] = os.getcwd()
        os.environ["barely_appdir"] = appdir

        make_dirs(appdir)
    else:
        print("barely :: could not find 'config.yaml'. Exiting")
        sys.exit()


def get_appdir():
    _platform = platform.system()

    if _platform == ("Linux" or "Darwin"):
        home = os.path.expanduser("~")
        return os.path.join(home, ".barely")
    elif _platform == "Windows":
        home = os.path.expandvars(r"%APPDATA%")
        return os.path.join(home, "barely")
    else:
        sys.exit("Running on unknown platform.")


def make_dirs(appdir):
    needed = [
        os.path.join("plugins", "content"),
        os.path.join("plugins", "backup"),
        os.path.join("plugins", "publication"),
        "blueprints"
    ]

    for path in needed:
        Path(os.path.join(appdir, path)).mkdir(parents=True, exist_ok=True)


def get_blueprints(blueprint=None):
    from glob import glob
    sys_bp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "blueprints")
    user_bp_path = os.path.join(get_appdir(), "blueprints")

    sys_bps = [os.path.basename(os.path.dirname(bp)) for bp in glob(sys_bp_path + os.sep + "*" + os.sep)]
    user_bps = [os.path.basename(os.path.dirname(bp)) for bp in glob(user_bp_path + os.sep + "*" + os.sep)]

    if blueprint:
        if blueprint in user_bps:
            return os.path.join(user_bp_path, blueprint)
        elif blueprint in sys_bps:
            return os.path.join(sys_bp_path, blueprint)
        else:
            print(f"barely :: no blueprint named {blueprint} exists.")
            sys.exit()
    return set(user_bps + sys_bps)


@click.group(invoke_without_command=True)
@click.pass_context
def run(context):
    """
    barely reduces static website development to its key parts,
    by automatically rendering jinja2 templates and Markdown content
    into HTML. A simple plugin interface allows for easy extensibility,
    and the built-in live web server makes on-the-fly development as
    comfortable as possible.
    """
    if context.invoked_subcommand is None:
        live()


@run.command()
@click.option("--blueprint", "-b", help="instantiate project from a blueprint", default="default")
@click.option("--webroot", "-w", help="location for the generated static files", default="webroot")
@click.option("--devroot", "-d", help="project directory, for development files", default="devroot")
def new(devroot, webroot, blueprint):
    """create a new barely project (optionally with a blueprint)"""
    import shutil
    import yaml
    make_dirs(get_appdir())
    blueprint_path = get_blueprints(blueprint)
    print("barely :: setting up new project with parameters:")

    os.makedirs(webroot)
    print(f"       ->   webroot: {webroot}")

    shutil.copytree(blueprint_path, devroot)
    print(f"       ->   devroot: {devroot}")
    print(f"       -> blueprint: {blueprint}")

    config = {
        "ROOT": {
            "DEV": os.path.abspath(os.path.join(os.getcwd(), devroot)),
            "WEB": os.path.abspath(os.path.join(os.getcwd(), webroot))
        }
    }
    with open(os.path.join(devroot, "config.yaml"), "w+") as file:
        file.write(yaml.dump(config))
    print("barely :: setting up basic config...")
    print("barely :: done.")
    os.chdir(devroot)


@run.command()
@click.option("--new", "-n", help="create a reusable blueprint from the current project")
def blueprints(new):
    """list all available blueprints, or create a new one"""
    make_dirs(get_appdir())
    if new:
        import shutil
        import yaml
        try:
            with open("config.yaml", "r") as file:
                meta_raw = file.read()
                devroot = yaml.safe_load(meta_raw)["ROOT"]["DEV"]
                new_path = os.path.join(get_appdir(), "blueprints", new)
            shutil.copytree(devroot, new_path)
            os.remove(os.path.join(new_path, "config.yaml"))
            print(f"barely :: blueprint \"{new}\" successfully created!")
        except FileNotFoundError:
            print("barely :: no valid project found. Can't create blueprint.")
        except FileExistsError:
            print("barely :: a blueprint with this name already exists.")

        try:
            shutil.rmtree(os.path.join(new_path, ".git"))
        except FileNotFoundError:
            pass
    else:
        blueprints = get_blueprints()
        print(f"barely :: found {len(blueprints)} blueprints:")
        for blueprint in blueprints:
            print(f"       -> {blueprint}")


@run.command()
@click.option("--verbose", "-v", help="print the logs from the live server", is_flag=True)
def live(verbose):
    """starts a live server, opens your project in the browser and auto-refreshes a page whenever it, its template, or the media it includes are modified."""
    init()

    from barely.core.EventHandler import EventHandler
    from barely.core.ChangeTracker import ChangeTracker
    from barely.plugins.PluginManager import PluginManager

    PM = PluginManager()
    EH = EventHandler()
    EH.init_pipeline(PM)

    CT = ChangeTracker()
    CT.register_handler(EH)
    CT.verbose = verbose

    CT.track()
    PM.finalize_content()
    aftermath(PM)


@run.command()
def rebuild():
    """(re)build the entire project"""
    init()

    from barely.core.EventHandler import EventHandler
    from barely.plugins.PluginManager import PluginManager

    PM = PluginManager()
    EH = EventHandler()
    EH.init_pipeline(PM)

    EH.force_rebuild()
    PM.finalize_content()

    aftermath(PM)


def aftermath(PM):
    print("barely ..")
    print("barely :: Do you want to Publish / Backup / do both?")
    action = input("       -> *[n]othing | [p]ublish | [b]ackup | [Y]do both :: ").lower()

    if action.startswith("p") or action.startswith("y"):
        print("barely :: publishing...")
        PM.hook_publication()
        print("       -> ...done.")
    if action.startswith("b") or action.startswith("y"):
        print("barely :: backuping...")
        PM.hook_backup()
        print("       -> ...done.")

    print("barely :: exited.")


@run.command()
@click.option("--keep-files", "-k", help="keep the files generated by the testsuite", is_flag=True)
@click.option("--verbose", "-v", help="diable the unittest buffer", is_flag=True)
def test(verbose, keep_files):
    """run the testsuite to verify the install"""
    import unittest
    import shutil

    #
    #   general setup
    #

    buffer = not verbose
    appdir = get_appdir()
    testdir = os.path.join(appdir, "TESTFILES")
    testsuite_dir = os.path.join(os.path.dirname(__file__), "tests")
    shutil.copytree(os.path.join(testsuite_dir, "ressources"), testdir)
    os.chdir(testdir)
    os.environ["barely"] = testdir
    os.environ["barely_appdir"] = appdir

    #
    #   barely core tests
    #

    loader = unittest.TestLoader()
    suite = loader.discover(testsuite_dir)
    runner = unittest.TextTestRunner(buffer=buffer)
    runner.run(suite)

    #
    #   system plugin tests
    #

    plugins_path = os.path.join(os.path.dirname(__file__), "plugins")
    plugin_loader = unittest.TestLoader()
    plugin_suite = plugin_loader.discover(plugins_path)
    plugin_runner = unittest.TextTestRunner(buffer=buffer)
    plugin_runner.run(plugin_suite)

    #
    #   cleanup
    #

    if not keep_files:
        os.chdir(appdir)
        shutil.rmtree(testdir)


if __name__ == "__main__":
    test()
