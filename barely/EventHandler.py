"""
Any actions concerning file translation
have to go through this class. It handles
move/delete events directly, and hands off
new/update events to the ProcessingPipeline
"""


class EventHandler():
    """ handle events, hand hem off, or diregard irrelevant ones """

    def __init__(self):
        pass

    def notify(self):
        """ anyone (but usually, the watchdog) can issue a notice of a file event """
        pass

    def force_rebuild(self):
        """ rebuild the entire project by first deleting the devroot, then marking every file as new """
        pass

    def _determine_type(self):
        """ determine the type of the file via its extension. return both """
        pass

    def _get_web_path(self):
        """ get where a file is supposed to go. depends on the type """
        pass

    def _delete(self):
        """ delete a file or dir """
        pass

    def _move(self):
        """ move a file or dir """
        pass
