#!/usr/bin/python3
"""State Module for the HBNB project."""

import models
from os import getenv
from models.base_model import Base, BaseModel
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Represents a state for a MySQL database.

    Attributes:
        __tablename__ (str): The name of the MySQL table storing states.
        name (sqlalchemy String): The state's name.
        cities (sqlalchemy relationship or property): The relationship with cities.
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    # Relationship for DBStorage
    cities = relationship("City", backref="state", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Retrieve related City objects for FileStorage.

            Returns:
                list: A list of City instances linked to this State.
            """
            return [
                city for city in models.storage.all(City).values()
                if city.state_id == self.id
            ]

