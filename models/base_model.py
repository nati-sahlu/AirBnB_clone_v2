#!/usr/bin/python3
"""Defines the BaseModel class with SQLAlchemy integration."""

from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models

# Define the declarative base for SQLAlchemy
Base = declarative_base()


class BaseModel:
    """A base class for all models in the AirBnB clone project."""

    # Define common attributes for all models
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new model instance."""
        if kwargs:
            # Handle attributes passed through kwargs
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            # Ensure id and timestamps are set if not provided
            if "id" not in kwargs:
                self.id = str(uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            # Default initialization for new instances
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def save(self):
        """Save the current instance to storage."""
        self.updated_at = datetime.utcnow()  # Update the timestamp
        models.storage.add(self)  # Add the instance to storage
        models.storage.commit()  # Commit the changes to the database

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = self.__class__.__name__
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["updated_at"] = self.updated_at.isoformat()
        # Remove SQLAlchemy state if present
        instance_dict.pop("_sa_instance_state", None)
        return instance_dict

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.remove(self)  # Remove the instance from storage

    def __str__(self):
        """Return a string representation of the instance."""
        cls_name = self.__class__.__name__
        attributes = {k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"}
        return "[{}] ({}) {}".format(cls_name, self.id, attributes)

