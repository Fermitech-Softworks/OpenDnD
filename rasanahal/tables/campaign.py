from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Campaign:
    __tablename__ = 'campaign'

    @declared_attr
    def cid(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def title(self):
        return Column(String, nullable=False)

    @declared_attr
    def players(self):
        return relationship("PartecipantAssociation", back_populates='campaign')

    @declared_attr
    def groups(self):
        return relationship("Group", back_populates="campaigns")

    @declared_attr
    def characters(self):
        return relationship("Character", back_populates="campaign")

    def __repr__(self):
        return "CAMPAIGN - {} {}".format(self.cid, self.title)