from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class ClassAssociation:
    __tablename__ = 'classassociation'

    @declared_attr
    def character_id(self):
        return Column(Integer, ForeignKey('character.cid'), primary_key=True)

    @declared_attr
    def class_id(self):
        return Column(Integer, ForeignKey('class.cid'), primary_key=True)

    @declared_attr
    def level(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def character(self):
        return relationship("Character", back_populates="classes")

    @declared_attr
    def class_(self):
        return relationship("Class", back_populates="characters")
