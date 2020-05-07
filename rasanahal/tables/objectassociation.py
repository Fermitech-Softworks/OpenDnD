from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class ObjectAssociation:
    __tablename__ = 'objectassociation'

    @declared_attr
    def character_id(self):
        return Column(Integer, ForeignKey('character.cid'), primary_key=True)

    @declared_attr
    def object_id(self):
        return Column(Integer, ForeignKey('object.oid'), primary_key=True)

    @declared_attr
    def quantity(self):
        return Column(Integer, nullable=False, default=1)

    @declared_attr
    def character(self):
        return relationship("Character", back_populates="inventory")

    @declared_attr
    def object(self):
        return relationship("Object", back_populates="characters")
