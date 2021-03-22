"""
Watchdog that can be started / stopped
by the user. Will notify ChangeHandler
of changes to files and dirs in devroot

Useful for live development
"""

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from barely.common.config import config
from barely.common.decorators import Singleton


@Singleton
class ChangeTracker:
    """ monitors the devroot for file and dir changes and notifies the ChangeHandler """

    def __init__(self, EH=None):
        if EH is not None:
            self.register_handler(EH)
        else:
            self.handler_availale = False

    def register_handler(self, EH):
        """ register an event handler. The EH gets notified about observed changes """
        patterns = "*"
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True
        handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

        handler.on_created = EH
        handler.on_deleted = EH
        handler.on_modified = EH
        handler.on_moved = EH

        """ set up the Observer """
        recursive = True
        self.observer = Observer()
        self.observer.schedule(handler, config["ROOT"]["DEV"], recursive=recursive)
        self.handler_availale = True

    def track(self, loop_action):
        """ start the watchdog configured above """
        if self.handler_availale:
            self.observer.start()
            try:
                while True:
                    while not self.observer.is_alive():
                        time.sleep(0.25)
                    loop_action()
            except KeyboardInterrupt:
                self.observer.stop()
            self.observer.join()
        else:
            raise Exception("No available handler. Not tracking.")
