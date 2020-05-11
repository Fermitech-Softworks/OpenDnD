from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class SkillAssociation:
    __tablename__ = 'skillassociation'

    @declared_attr
    def skill_id(self):
        return Column(Integer, ForeignKey('skill.sid'), primary_key=True)

    @declared_attr
    def character_id(self):
        return Column(Integer, ForeignKey('character.cid'), primary_key=True)

    @declared_attr
    def level(self):  # 0=half, 1= full, 2= expertise
        return Column(Integer, nullable=False)

    @declared_attr
    def skill(self):
        return relationship("Skill", back_populates="characters")

    @declared_attr
    def character(self):
        return relationship("Character", back_populates="skills")
