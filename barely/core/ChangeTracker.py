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


class ChangeTracker:
    """ monitors the devroot for file and dir changes and notifies the ChangeHandler """

    def __init__(self, EH=None):
        if EH is not None:
            self.register_handler(EH)
        else:
            self.handler_available = False
        self.eventbuffer = []

    def register_handler(self, EH):
        """ register an event handler. The EH gets notified about observed changes """
        patterns = "*"
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True
        handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

        handler.on_created = self.buffer
        handler.on_deleted = self.buffer
        handler.on_modified = self.buffer
        handler.on_moved = self.buffer
        self.EH = EH

        """ set up the Observer """
        recursive = True
        self.observer = Observer()
        self.observer.schedule(handler, config["ROOT"]["DEV"], recursive=recursive)

        self.handler_available = True

    def track(self, loop_action=lambda: None):
        """ start the watchdog configured above """
        if self.handler_available:
            self.observer.start()
            print("barely :: started tracking...")
            try:
                while True:
                    time.sleep(0.25)
                    loop_action()
                    self.empty_buffer()
            except KeyboardInterrupt:
                self.observer.stop()
                print("barely :: stopped tracking.")
            self.observer.join()
        else:
            raise Exception("No available handler. Not tracking.")

    def buffer(self, event):
        try:
            relevant_path = event.dest_path
        except AttributeError:
            relevant_path = event.src_path
        event.relevant_path = relevant_path

        irrelevant = []
        for older in self.eventbuffer:
            if type(event) is type(older) and event.relevant_path == older.relevant_path:
                irrelevant.append(older)
        for i in irrelevant:
            self.eventbuffer.remove(i)
        self.eventbuffer.append(event)

    def empty_buffer(self):
        for event in self.eventbuffer:
            self.EH.notify(event)
        self.eventbuffer = []
