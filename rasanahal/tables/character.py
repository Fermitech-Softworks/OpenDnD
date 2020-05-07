from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Character:
    __tablename__ = 'character'

    @declared_attr
    def cid(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def is_npc(self):
        return Column(Boolean, nullable=False)

    @declared_attr
    def name(self):
        return Column(String, nullable=False)

    @declared_attr
    def race_id(self):
        return Column(Integer, ForeignKey('race.rid'))

    @declared_attr
    def race(self):
        return relationship("Race", back_populates="characters")

    @declared_attr
    def level(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def maxhp(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def currenthp(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def proficiency(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def strength(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def dexterity(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def constitution(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def intelligence(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def wisdom(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def charisma(self):
        return Column(Integer, nullable=False)

    @declared_attr
    def strength_st(self):
        return Column(Boolean, nullable=False)

    @declared_attr
    def dexterity_st(self):
        return Column(Boolean, nullable=False)

    @declared_attr
    def constitution_st(self):
        return Column(Boolean, nullable=False)

    @declared_attr
    def intelligence_st(self):
        return Column(Boolean, nullable=False)

    @declared_attr
    def wisdom_st(self):
        return Column(Boolean, nullable=False)

    @declared_attr
    def charisma_st(self):
        return Column(Boolean, nullable=False)

    @declared_attr
    def notes(self):
        return Column(String, nullable=True)

    @declared_attr
    def owner_id(self):
        return Column(Integer, ForeignKey('users.uid'))

    @declared_attr
    def owner(self):
        return relationship("User", backref="characters")

    @declared_attr
    def campaign_id(self):
        return Column(Integer, ForeignKey('campaign.cid'))

    @declared_attr
    def campaign(self):
        return relationship("Campaign", back_populates="characters")

    @declared_attr
    def skills(self):
        return relationship("SkillAssociation", back_populates="character")

    @declared_attr
    def inventory(self):
        return relationship("ObjectAssociation", back_populates="character")

    @declared_attr
    def classes(self):
        return relationship("ClassAssociation", back_populates="character")

    @declared_attr
    def spells(self):
        return relationship("SpellAssociation", back_populates="character")

    def json(self, minimal):
        return {
            'id': self.cid,
            'is_npc': self.is_npc,
            'name': self.name,
            'race': self.race.json(),
            'level': self.level,
            'maxhp': self.maxhp,
            'currenthp': self.currenthp,
            'proficiency': self.proficiency,
            'attributes': {
                'str': self.strength,
                'dex': self.dexterity,
                'con': self.constitution,
                'int': self.intelligence,
                'wis': self.wisdom,
                'cha': self.charisma
            },
            'ts': {
                'str': self.strength_st,
                'dex': self.dexterity_st,
                'con': self.constitution_st,
                'int': self.intelligence_st,
                'wis': self.wisdom_st,
                'cha': self.charisma_st
            },
            'notes': self.notes,
            'owner': self.owner.uid if minimal else self.owner.json(),
            'campaigns': [campaign.cid if minimal else campaign.json(True) for campaign in self.campaign],
            'classes': [{'id': cla.class_.cid, 'level': cla} if minimal else cla.class_.json(True) for cla in self.classes],
            'inventory': [{'id': obj.object_.oid, 'qty': obj.quantity} if minimal else obj.object_.json(True) for obj in self.inventory],
            'spells': [{'id': s.spell.sid} if minimal else s.spell.json(True) for s in self.spells],
            'skills': [{'id': s.skill.id, 'level': s.level} if minimal else s.skill.json(True) for s in self.skills]

        }
