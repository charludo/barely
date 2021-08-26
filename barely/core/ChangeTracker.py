"""
Watchdog that can be started / stopped
by the user. Will notify ChangeHandler
of changes to files and dirs in devroot

Useful for live development
"""


import time
import signal
import logging
from livereload import Server
from multiprocessing import Process
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from barely.common.config import config


def empty_func():
    return None


class ChangeTracker:
    """ monitors the devroot for file and dir changes and notifies the ChangeHandler """
    logger = logging.getLogger("base.core")
    logger_indented = logging.getLogger("indented")

    def __init__(self, EH=None):
        self.logger.debug("new ChangeTracker created")
        if EH is not None:
            self.register_handler(EH)
        else:
            self.handler_available = False
        self.eventbuffer = []
        self.verbose = False

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
        self.logger.debug("registered and configured a change-handler")

        """ set up the Observer """
        recursive = True
        self.observer = Observer()
        self.observer.schedule(handler, config["ROOT"]["DEV"], recursive=recursive)
        self.logger.debug("configured an observer")

        self.handler_available = True

    def track(self, loop_action=empty_func):
        """ start the watchdog configured above """
        if self.handler_available:
            # setup the livereload server
            server = Server()
            if not self.verbose:
                server._setup_logging = empty_func
            server.watch(config["ROOT"]["WEB"], delay=0.1)
            self.liveserver = Process(target=server.serve, kwargs={"root": config["ROOT"]["WEB"], "open_url_delay": 1})

            self.liveserver.start()
            self.observer.start()
            self.tracking = True
            self.logger.debug("liveserver and observer started")
            self.logger.info("started tracking...")

            # handle SIGINTs. Store the original to later reuse it.
            self.original_sigint = signal.getsignal(signal.SIGINT)
            signal.signal(signal.SIGINT, self.stop)

            # check buffer every 0.2s; should be enough to catch duplicate events
            while self.tracking:
                time.sleep(0.2)
                loop_action()
                self.empty_buffer()
        else:
            raise Exception("No available handler. Not tracking.")

    def buffer(self, event):
        # spares the hassle of dealing with different types of events.
        event.relevant_path = event.dest_path if hasattr(event, "dest_path") else event.src_path
        self.logger.debug(f"buffered event at {event.relevant_path}")
        i = 0
        while i < len(self.eventbuffer):
            older = self.eventbuffer[i]
            if type(event) is type(older) and event.relevant_path == older.relevant_path:
                self.eventbuffer.pop(i)
                self.logger.debug("removed duplicate older event")
            i += 1
        self.eventbuffer.append(event)

    def empty_buffer(self):
        for event in self.eventbuffer:
            self.EH.notify(event)
        self.eventbuffer = []

    def stop(self, signum, frame):
        self.logger.debug("received signal to stop tracking")
        signal.signal(signal.SIGINT, self.original_sigint)

        self.tracking = False
        self.observer.stop()
        self.observer.join()
        self.liveserver.join()

        print()
        print("\033[A\033[A")
        self.logger.info("stopped tracking.")
