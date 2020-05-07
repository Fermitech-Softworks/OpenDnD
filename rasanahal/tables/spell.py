from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Spell:
    __tablename__ = 'spell'

    @declared_attr
    def sid(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def name(self):
        return Column(String, nullable=False, unique=True)

    @declared_attr
    def school(self):
        return Column(String, nullable=False)

    @declared_attr
    def comp(self):
        return Column(String, nullable=False)

    @declared_attr
    def desc(self):
        return Column(String, nullable=False)

    @declared_attr
    def die(self):
        return Column(String)

    @declared_attr
    def characters(self):
        return relationship("SpellAssociation", back_populates='spell')

    def json(self, minimal):
        return {
            'id': self.oid,
            'name': self.name,
            'school': self.school,
            'comp': self.comp,
            'die': self.die,
            'desc': self.desc,
            'characters': [char.character.cid if minimal else char.character.json(True) for char in self.characters]
        }
