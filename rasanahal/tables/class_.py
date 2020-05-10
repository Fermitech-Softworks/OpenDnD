from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Class:
    __tablename__ = 'class'

    @declared_attr
    def cid(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def name(self):
        return Column(String, nullable=False, unique=True)

    @declared_attr
    def desc(self):
        return Column(String, nullable=False)

    @declared_attr
    def characters(self):
        return relationship("ClassAssociation", back_populates='class_')

    def json(self, minimal):
        return {
            'id': self.cid,
            'name': self.name,
            'desc': self.desc,
            'characters': [char.character.cid if minimal else char.character.json(True) for char in self.characters]
        }
