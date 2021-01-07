"""
Watchdog that can be started / stopped
by the user. Will notify ChangeHandler
of changes to files and dirs in devroot

Useful for live development
"""

import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileCreatedEvent, DirCreatedEvent
from watchdog.events import FileModifiedEvent
from watchdog.events import FileDeletedEvent, DirDeletedEvent
from watchdog.events import FileMovedEvent, DirMovedEvent

from .changehandler import ChangeHandler
from barely.common.config import config
from barely.common.utils import dev_to_web
from barely.common.decorators import Singleton


@Singleton
class ChangeTracker:
    """ monitors the devroot for file and dir changes and notifies the ChangeHandler """

    handler = None
    observer = None
    CH = ChangeHandler.instance()

    silent = False
    template_dir = ""

    def __init__(self):
        path = config["ROOT"]["DEV"]
        self.setup_eventhandler(path)

    def setup_eventhandler(self, path):
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

        recursive = True
        self.observer = Observer()
        self.observer.schedule(self.handler, path, recursive=recursive)

        self.template_dir = os.path.join(path, "templates")

    def mute(self):
        self.silence = True

    def _notify(self, event):
        src_dev = event.src_path
        src_web = dev_to_web(src_dev)
        try:
            dest_dev = event.dest_path
            dest_web = dev_to_web(dest_dev)
        except AttributeError:
            dest_dev = None
            dest_web = None

        if self.template_dir in src_dev and not isinstance(event, FileDeletedEvent) and not isinstance(event, DirDeletedEvent):
            if dest_dev is None:
                affected = src_dev
            else:
                affected = dest_dev
            result = f"Change to {affected} affected:"
            for pair in self.CH.notify_changed_template(affected, self.template_dir):
                result += "\n* {pair[0]} -> {pair[1]}"
        elif isinstance(event, FileCreatedEvent):
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
            result = None

        if result and not self.silence:
            print(f"ChangeTracker:: {result}")

    def start(self, loop_action):
        """ start the watchdog configured above """
        if not self.silence:
            print("ChangeTracker running, monitoring {0}:".format(config["ROOT"]["DEV"]))
        self.observer.start()
        try:
            while True:
                while not self.observer.is_alive():
                    time.sleep(0.25)
                loop_action()
        except KeyboardInterrupt:
            self.observer.stop()
            if not self.silence:
                print("\nChangeTracker stopped.")
        self.observer.join()

    def stop(self):
        """ stop the watchdog """
        self.observer.stop()
        self.observer.join()
        if not self.silence:
            print("\nChangeTracker stopped.")
