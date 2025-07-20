#!/usr/bin/env python3
"""
This module initializes the storage system for the application.

It imports the FileStorage class from the storage.file_storage module,
creates a global instance of FileStorage, and reloads the storage to
ensure data is loaded into memory at startup.
"""

from .storage.file_storage import FileStorage


store = FileStorage()
store.reload()
