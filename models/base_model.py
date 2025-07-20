#!/usr/bin/env python3
"""
base_model.py

This module defines the BaseModel class, which serves as a foundational
class for other classes in a system. It includes basic attributes like id,
creation time, and update time, and provides utility methods for
serialization and deserialization of instances.
"""
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """
    BaseModel class that provides basic attributes and methods for
    other classes to inherit from.

    Attributes:
        id (str): Unique identifier for the instance.
        created_at (datetime): Timestamp of when the instance was created.
        updated_at (datetime): Timestamp of the last update to the instance.
    """
    def __init__(self):
        """
        Initializes a new instance of BaseModel with a unique ID and
        timestamps for creation and last update.
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        models.store.new(self)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.

        Returns:
            str: A string in the format
            '[<class name>] (<id>) <attribute dictionary>'
        """
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def to_dict(self):
        """
        Serializes the instance to a dictionary format suitable for
        storage or transmission.

        Returns:
            dict: A dictionary containing all instance attributes, with
            datetime objects converted to ISO format strings, and an
            additional '__class__' key with the class name.
        """
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__

        for key, value in dictionary.items():
            if isinstance(value, datetime):
                dictionary[key] = value.isoformat()

        return dictionary

    @classmethod
    def from_dict(cls, data):
        """
        Deserializes a dictionary to create a BaseModel instance.

        Args:
            data (dict): A dictionary representation of a BaseModel
            instance, typically created using to_dict().

        Returns:
            BaseModel: A new instance populated with values from the
            provided dictionary.
        """
        obj = cls.__new__(cls)  # bypass init
        for key, value in data.items():
            if key in ['created_at', 'updated_at']:
                setattr(obj, key, datetime.fromisoformat(value))
            elif key != '__class__':
                setattr(obj, key, value)
        return obj

    def save(self):
        self.updated_at = datetime.now()
        models.store.save()
