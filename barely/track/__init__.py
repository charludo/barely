"""
Subpackage tasked with tracking
file changes in the devroot, as
well as handling changes (either
by copying/deleting/... files directly,
or by handing the task off to the
render subpackage)
"""
from .changehandler import ChangeHandler
from .changetracker import ChangeTracker


global CHANGEHANDLER
CHANGEHANDLER = ChangeHandler.instance()

global CHANGETRACKER
CHANGETRACKER = ChangeTracker.instance()
