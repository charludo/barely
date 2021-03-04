"""
Any actions concerning file translation
have to go through this class. It handles
move/delete events directly, and hands off
new/update events to the ProcessingPipeline
"""

from watchdog.events import FileCreatedEvent, FileModifiedEvent
from watchdog.events import FileDeletedEvent, DirDeletedEvent
from watchdog.events import FileMovedEvent, DirMovedEvent


class EventHandler():
    """ handle events, hand hem off, or diregard irrelevant ones """

    def __init__(self):
        pass

    def notify(self, event):
        """ anyone (but usually, the watchdog) can issue a notice of a file event """
        src_dev = event.src_path
        src_web = self._get_web_path(src_dev)

        if self.template_dir in src_dev and not isinstance(event, FileDeletedEvent) and not isinstance(event, DirDeletedEvent):
            # TODO: _get_affected; jeweils sich selbst notifyen mit einem Event
            pass
        elif "config.yaml" in src_dev or "metadata.yaml" in src_dev:
            # don't do anything. These changes don't have to be tracked.
            pass
        elif "_*.md" in src_dev:
            # TODO: _get_parent_page; diese notifyen
            pass
        elif isinstance(event, FileDeletedEvent) or isinstance(event, DirDeletedEvent):
            self._delete(src_web)
        elif isinstance(event, FileMovedEvent) or isinstance(event, DirMovedEvent):
            dest_web = self._get_web_path(event.dest_path)
            self._move(src_web, dest_web)
        elif isinstance(event, FileCreatedEvent) or isinstance(event, FileModifiedEvent):
            type, extension = self._determine_type()
            item = {
                "origin": src_dev,
                "destination": src_web,
                "type": type,
                "extension": extension
            }
            self.pipeline.process([item])
        else:
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

    def _get_affected(self):
        """ yield the paths of all files that rely on a certain template """
        pass

    def _get_parent_page(self):
        """ yield the path of the parent of a subpage """
        pass

    def _delete(self, path):
        """ delete a file or dir """
        pass

    def _move(self, fro, to):
        """ move a file or dir """
        pass
