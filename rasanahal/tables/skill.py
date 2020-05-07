from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Skill:
    __tablename__ = 'skill'

    @declared_attr
    def sid(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def name(self):
        return Column(String, nullable=False)

    @declared_attr
    def attribute(self):
        return Column(Integer, nullable=False)  # 1:STR, 2:DEX, 3:COS, 4:INT, 6:CHA, 7:WIS

    @declared_attr
    def desc(self):
        return Column(String, nullable=True)

    @declared_attr
    def characters(self):
        return relationship("SkillAssociation", back_populates="skill")
