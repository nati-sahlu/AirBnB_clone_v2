#!/usr/bin/python3
"""Manages storage of objects in JSON format."""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Handles the storage and retrieval of objects in JSON format."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects, optionally filtered by class."""
        if cls is not None:
            if isinstance(cls, str):
                cls = globals().get(cls, None)
            return {key: obj for key, obj in self.__objects.items() if isinstance(obj, cls)}
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage."""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Saves the current objects to the JSON file."""
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump({key: obj.to_dict() for key, obj in self.__objects.items()}, f)

    def reload(self):
        """Loads objects from the JSON file into storage."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for obj_dict in data.values():
                    class_name = obj_dict["__class__"]
                    del obj_dict["__class__"]
                    self.new(globals()[class_name](**obj_dict))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from the storage."""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Reloads the storage from the file."""
        self.reload()

