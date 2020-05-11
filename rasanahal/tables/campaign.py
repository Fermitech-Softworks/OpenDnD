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
        return relationship("Group", back_populates="campaign")

    @declared_attr
    def characters(self):
        return relationship("Character", back_populates="campaign")

    def __repr__(self):
        return "CAMPAIGN - {} {}".format(self.cid, self.title)

    def json(self, minimal):
        return {
            'id': self.cid,
            'title': self.title,
            'players': [player.json() for player in self.players],
            'characters': [character.cid if minimal else character.json(True) for character in self.characters],
            'groups': [group.gid if minimal else group.json(True) for group in self.groups]
        }

    def locate_gm(self):
        for connection in self.players:
            if connection.is_gm:
                return connection.user_id
