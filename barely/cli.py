"""
functions that are available to be called
from the cli by the user.
"""
import os
import sys
import click
import platform
import logging
import coloredlogs
from pathlib import Path
from click_default_group import DefaultGroup


def setup_loggers(level):
    # filter t only show last part of logger name
    class ShortNameFilter(logging.Filter):
        def filter(self, record):
            record.name = record.name.rsplit('.', 1)[-1]
            return True

    base = logging.getLogger("base")
    format = "[barely][%(name)6s][%(levelname)5s] :: %(message)s"
    style = coloredlogs.DEFAULT_FIELD_STYLES | {"levelname": {"bold": False, "color": 244}}
    coloredlogs.install(level=level, logger=base, fmt=format, field_styles=style)

    for handler in base.handlers:
        handler.addFilter(ShortNameFilter())

    global logger
    logger = logging.getLogger("base.core")

    global logger_indented
    logger_indented = logging.getLogger("indented")
    format_indented = "                        -> %(message)s"
    coloredlogs.install(level=level, logger=logger_indented, fmt=format_indented)

    logger.debug("Logging setup complete")


def init():
    logger.debug("initializing barely")

    # try to find the config.yaml
    if os.path.exists("config.yaml"):
        logger.debug("found barely config file")

        # export the cwd as an environment variable
        appdir = get_appdir()
        os.environ["barely"] = os.getcwd()
        os.environ["barely_appdir"] = appdir

        make_dirs(appdir)
    else:
        logger.error("could not find 'config.yaml'. Exiting")
        sys.exit()


def get_appdir():
    _platform = platform.system()

    if _platform == ("Linux" or "Darwin"):
        logger.debug("platform: Unix-like")
        home = os.path.expanduser("~")
        return os.path.join(home, ".barely")
    elif _platform == "Windows":
        logger.debug("platform: Windows")
        home = os.path.expandvars(r"%APPDATA%")
        os.environ["PYTHONIOENCODING"] = "utf-8"
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
        logger.debug(f"checked / created {path}")

    logger.debug("created all required dirs")


def get_blueprints(blueprint=None):
    from glob import glob
    sys_bp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "blueprints")
    user_bp_path = os.path.join(get_appdir(), "blueprints")

    sys_bps = [os.path.basename(os.path.dirname(bp)) for bp in glob(sys_bp_path + os.sep + "*" + os.sep)]
    user_bps = [os.path.basename(os.path.dirname(bp)) for bp in glob(user_bp_path + os.sep + "*" + os.sep)]

    logger.debug(f"looking for blueprints in: {sys_bp_path}")
    logger.debug(f"looking for blueprints in: {user_bp_path}")

    if blueprint:
        if blueprint in user_bps:
            logger.debug(f"found {blueprint} in user blueprints")
            return os.path.join(user_bp_path, blueprint)
        elif blueprint in sys_bps:
            logger.debug(f"found {blueprint} in system blueprints")
            return os.path.join(sys_bp_path, blueprint)
        else:
            logger.error(f"no blueprint named {blueprint} exists.")
            sys.exit()
    return set(user_bps + sys_bps)


@click.group(cls=DefaultGroup, default='live', default_if_no_args=True)
@click.option("--debug", "-d", help="set logging level to debug", is_flag=True)
@click.pass_context
def run(context, debug):
    """
    barely reduces static website development to its key parts,
    by automatically rendering jinja2 templates and Markdown content
    into HTML. A simple plugin interface allows for easy extensibility,
    and the built-in live web server makes on-the-fly development as
    comfortable as possible.
    """
    setup_loggers("DEBUG" if debug else "INFO")


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
    logger.info("setting up new project with parameters:")

    os.makedirs(webroot)
    logger_indented.info(f"  webroot: {webroot}")

    shutil.copytree(blueprint_path, devroot)
    logger_indented.info(f"  devroot: {devroot}")
    logger_indented.info(f"blueprint: {blueprint}")

    config = {
        "ROOT": {
            "DEV": os.path.abspath(os.path.join(os.getcwd(), devroot)),
            "WEB": os.path.abspath(os.path.join(os.getcwd(), webroot))
        }
    }
    with open(os.path.join(devroot, "config.yaml"), "w+") as file:
        file.write(yaml.dump(config))
    logger.info("setting up basic config...")
    logger.info("done.")
    os.chdir(devroot)


@run.command()
@click.option("--new", "-n", help="create a reusable blueprint from the current project")
def blueprints(new):
    """list all available blueprints, or create a new one"""
    make_dirs(get_appdir())
    if new:
        import shutil
        import yaml

        logger.debug("started blueprint creation process")
        try:
            with open("config.yaml", "r") as file:
                meta_raw = file.read()
                devroot = yaml.safe_load(meta_raw)["ROOT"]["DEV"]
                new_path = os.path.join(get_appdir(), "blueprints", new)
            shutil.copytree(devroot, new_path)
            os.remove(os.path.join(new_path, "config.yaml"))
            logger.info(f"blueprint \"{new}\" successfully created!")
        except FileNotFoundError:
            logger.error("no valid project found. Can't create blueprint.")
        except FileExistsError:
            logger.error("a blueprint with this name already exists.")

        try:
            shutil.rmtree(os.path.join(new_path, ".git"))
            logger.debug("deleted git repo found in blueprint")
        except FileNotFoundError:
            pass
    else:
        blueprints = get_blueprints()
        logger.info(f"found {len(blueprints)} blueprints:")
        for blueprint in blueprints:
            logger_indented.info(f"{blueprint}")


@run.command()
@click.option("--verbose", "-v", help="print the logs from the live server", is_flag=True)
def live(verbose):
    """starts a live server, opens your project in the browser and auto-refreshes a page whenever it, its template, or the media it includes are modified."""
    init()
    from barely.core.EventHandler import EventHandler
    from barely.core.ChangeTracker import ChangeTracker
    from barely.plugins.PluginManager import PluginManager

    logger.debug("starting barely in live mode")

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
@click.option("--light", "-l", help="don't clean existing files, and skip image rebuilds", is_flag=True)
@click.option("--partial", "-p", help="specify file or directory to rebuild instead of devroot", default="devroot")
@click.option("--start", "-s", help="after rebuilding, start the web server", is_flag=True)
@click.pass_context
def rebuild(ctx, start, partial, light):
    """(re)build the entire project"""
    init()

    from barely.core.EventHandler import EventHandler
    from barely.plugins.PluginManager import PluginManager

    logger.debug("started a rebuild")

    PM = PluginManager()
    EH = EventHandler()
    EH.init_pipeline(PM)

    EH.force_rebuild(partial, light)
    PM.finalize_content()

    if start:
        ctx.invoke(live)
    else:
        aftermath(PM)


def aftermath(PM):
    logger.debug("exited main program, starting aftermath")
    logger.info("..")
    logger_indented.info("Do you want to Publish / Backup / do both?")
    action = input("                        -> *[n]othing | [p]ublish | [b]ackup | [Y]do both :: ").lower()

    if action.startswith("p") or action.startswith("y"):
        logger_indented.info("publishing...")
        PM.hook_publication()
        logger_indented.info("...done.")
    if action.startswith("b") or action.startswith("y"):
        logger.info("backuping...")
        PM.hook_backup()
        logger_indented.info("...done.")

    logger.info("exited.")


@run.command()
@click.option("--page", "-p", help="specify a page to be evaluated other than the root", default="")
def lighthouse(page):
    """use Google Lighthouse to evaluate a page for SEO- and accessibility scores"""
    import subprocess
    version = subprocess.run(["lighthouse", "--version"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

    if not version[0].isdigit():
        logger.error("lighthouse could not be found. Ensure node, lighthouse, and chrome/chromium are installed.")
        sys.exit()
    else:
        import yaml
        import webbrowser
        from livereload import Server
        from multiprocessing import Process

        init()
        logger.info(f"Starting evaluation using lighthouse {version}...")

        # start the webserver
        with open("config.yaml", "r") as file:
            raw = file.read()
            loaded = yaml.safe_load(raw)
            webroot = loaded["ROOT"]["WEB"]
            devroot = loaded["ROOT"]["DEV"]

        server = Server()
        server._setup_logging = lambda: None
        liveserver = Process(target=server.serve, kwargs={"root": webroot})
        liveserver.start()

        # start lighthouse
        target_file = os.path.join(devroot, "lighthouse_report.html")
        if len(page) and not page.startswith("/"):
            page = "/" + page
        subprocess.call(f"lighthouse http://127.0.0.1:5500{page} --output-path {target_file} --chrome-flags=\"--headless\" --quiet", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        # stop the webserver
        liveserver.kill()
        logger.info("Finished the evaluation! Opening the result now.")

        # open the report
        webbrowser.open("file://" + target_file)


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
    logger.info("Setting up test environment...")

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
    logger.info("Starting barely core tests...")

    loader = unittest.TestLoader()
    suite = loader.discover(testsuite_dir)
    runner = unittest.TextTestRunner(buffer=buffer)
    runner.run(suite)

    #
    #   system plugin tests
    #
    logger.info("Starting system plugin tests...")

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
        logger.info("Cleaning up... Finished")


if __name__ == "__main__":
    setup_loggers("INFO")
    test()
