from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class SpellAssociation:
    __tablename__ = 'spellassociation'

    @declared_attr
    def character_id(self):
        return Column(Integer, ForeignKey('character.cid'), primary_key=True)

    @declared_attr
    def spell_id(self):
        return Column(Integer, ForeignKey('spell.sid'), primary_key=True)

    @declared_attr
    def character(self):
        return relationship("Character", back_populates="spells")

    @declared_attr
    def spell(self):
        return relationship("Spell", back_populates="characters")
