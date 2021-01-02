"""
TODO:
- templates watchdog - am einfachsten, alle renderables zu re-rendern? (zumindest vorübergehend)

- Renderer liest Mediendateien, übergibt "media" an template
- Minimizer für JS, CSS, IMG

- modular pages
- contact forms
- res einbinden in unter-templates
- ftp upload (?)
- blueprints erstellen
"""
import os
os.environ["BASEDIR"] = os.path.abspath(os.getcwd()) + "/testing"
if True:
    from src.changehandler import ChangeHandler
    from src.changetracker import ChangeTracker

ch = ChangeHandler()
tracker = ChangeTracker(ch)
tracker.start()
