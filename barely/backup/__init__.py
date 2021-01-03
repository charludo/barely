"""
Subpackage that deals with
creating and restoring backups.
"""

from .backupmanager import BackupManager

global BACKUPMANAGER
BACKUPMANAGER = BackupManager.instance()
