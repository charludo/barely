"""
Watchdog that can be started / stopped
by the user. Will notify ChangeHandler
of changes to files and dirs in devroot

Useful for live development
"""

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileCreatedEvent, DirCreatedEvent
from watchdog.events import FileModifiedEvent
from watchdog.events import FileDeletedEvent, DirDeletedEvent
from watchdog.events import FileMovedEvent, DirMovedEvent

from barely.common.config import config
from barely.common.utils import dev_to_web
from barely.common.decorators import Singleton


@Singleton
class ChangeTracker:
    """ monitors the devroot for file and dir changes and notifies the ChangeHandler """

    handler = None
    observer = None

    CH = None

    def __init__(self, changehandler):

        self.CH = changehandler

        """ set up the Event Handler """
        patterns = "*"
        ignore_patterns = ""
        ignore_directories = False
        case_sensitive = True
        self.handler = PatternMatchingEventHandler(patterns,
                                                   ignore_patterns,
                                                   ignore_directories,
                                                   case_sensitive)

        self.handler.on_created = self._notify
        self.handler.on_deleted = self._notify
        self.handler.on_modified = self._notify
        self.handler.on_moved = self._notify

        """ set up the Observer """
        path = config["ROOT"]["DEV"]
        recursive = True
        self.observer = Observer()
        self.observer.schedule(self.handler, path, recursive=recursive)

    def _notify(self, event):
        src_dev = event.src_path
        src_web = dev_to_web(src_dev)
        try:
            dest_dev = event.dest_path
            dest_web = dev_to_web(dest_dev)
        except AttributeError:
            pass

        if isinstance(event, FileCreatedEvent):
            result = self.CH.notify_added_file(src_dev, src_web)
        elif isinstance(event, DirCreatedEvent):
            result = self.CH.notify_added_dir(src_web)
        elif isinstance(event, FileDeletedEvent) or isinstance(event, DirDeletedEvent):
            result = self.CH.notify_deleted(src_web)
        elif isinstance(event, FileMovedEvent):
            result = self.CH.notify_moved_file(src_web, dest_dev, dest_web)
        elif isinstance(event, DirMovedEvent):
            result = self.CH.notify_moved_dir(src_web, dest_web)
        elif isinstance(event, FileModifiedEvent):
            result = self.CH.notify_modified(src_dev, src_web)
        else:
            pass

        if result:
            print(f"ChangeTracker:: {result}")

    def start(self):
        """ start the watchdog configured above """
        print("ChangeTracker running, monitoring {0}:".format(config["ROOT"]["DEV"]))
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            self.observer.join()
            print("\nChangeTracker stopped.")

    def stop(self):
        """ stop the watchdog """
        self.observer.stop()
        self.observer.join()
        print("\nChangeTracker stopped.")
