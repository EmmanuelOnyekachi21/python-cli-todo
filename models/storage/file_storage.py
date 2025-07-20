#!/usr/bin/env python3
"""
file_storage.py
This module provides the FileStorage class for serializing and deserializing
objects to and from a JSON file. It is designed to persist application data
such as tasks in a file-based storage system.
"""
import json
from models.task import Task


class FileStorage:
    """
    Handles storage and retrieval of objects using a JSON file.
    The FileStorage class manages the serialization and deserialization of
    objects, allowing them to be saved to and loaded from a file. It supports
    adding new objects, retrieving all stored objects, saving objects to disk,
    and reloading objects from disk.
    """
    __file_path = 'file.json'
    __objects = {}

    models = {
        'Task': Task
    }

    def all(self):
        """
        Returns a dictionary of all stored objects.
        Returns:
            dict: All objects currently stored in memory.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to the storage dictionary.
        If an object with the same key exists, it is replaced.
        Args:
            obj: The object to be added to storage.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"

        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes all objects to the JSON file.
        Converts all objects to dictionaries and writes them to the file
        specified by __file_path.
        """
        new_dictionary = {
            key: obj.to_dict() for key, obj in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(new_dictionary, f, indent=4)

    def reload(self):
        """
        Deserializes objects from the JSON file and loads them into memory.
        If the file does not exist, a message is printed indicating that no
        tasks have been created yet.
        """
        try:
            with open(FileStorage.__file_path, 'r') as f:
                data = json.load(f)

                for key, value in data.items():
                    class_name = key.split('.')[0]
                    cls = FileStorage.models[class_name]
                    obj = cls.from_dict(value)
                    FileStorage.__objects[key] = obj
                    # print({key: obj})
        except FileNotFoundError:
            # print("No task created yet")
            pass
    
    def delete(self, obj):
        """
        Removes the specified object from the storage.
        Args:
            obj: The object to be deleted. Must have 'id' attribute.
        Returns:
            None
        """
        
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects.pop(key, None)
