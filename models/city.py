#!/usr/bin/python3
"""City Module for the HBNB project."""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Represents a city in the database.

    Attributes:
        __tablename__ (str): Name of the MySQL table storing cities.
        name (sqlalchemy String): City's name.
        state_id (sqlalchemy String): ID of the associated state.
    """

    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)

    # Establish relationship with Place (if applicable)
    places = relationship("Place", backref="cities", cascade="delete")

