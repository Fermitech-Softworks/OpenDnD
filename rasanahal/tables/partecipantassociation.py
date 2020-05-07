from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class PartecipantAssociation:
    __tablename__ = 'partecipantassociation'

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey('users.uid'), primary_key=True)

    @declared_attr
    def campaign_id(self):
        return Column(Integer, ForeignKey('campaign.cid'), primary_key=True)

    @declared_attr
    def is_gm(self):
        return Column(Boolean, nullable=False, default=False)

    @declared_attr
    def user(self):
        return relationship("User", backref='partecipations')

    @declared_attr
    def campaign(self):
        return relationship("Campaign", back_populates='players')
