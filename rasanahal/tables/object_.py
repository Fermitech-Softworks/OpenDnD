from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Object:
    __tablename__ = 'object'

    @declared_attr
    def oid(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def name(self):
        return Column(String, nullable=False, unique=True)

    @declared_attr
    def cost(self):
        return Column(String)

    @declared_attr
    def desc(self):
        return Column(String, nullable=False)

    @declared_attr
    def characters(self):
        return relationship("ObjectAssociation", back_populates='object')
