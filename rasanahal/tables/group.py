from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Group:
    __tablename__ = 'group'

    @declared_attr
    def gid(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def name(self):
        return Column(String, nullable=False)

    @declared_attr
    def campaign_id(self):
        return Column(Integer, ForeignKey('campaign.cid'))

    @declared_attr
    def campaign(self):
        return relationship("Campaign", back_populates="groups")

    @declared_attr
    def active(self):
        return Column(Boolean, nullable=False)

    @declared_attr
    def isolated(self):
        return Column(Boolean, nullable=False)

    @declared_attr
    def users(self):
        return relationship("GroupAssociation", back_populates='group')

    @declared_attr
    def messages(self):
        return relationship("Message", back_populates="group")

    def json(self, minimal):
        return {
            'id': self.gid,
            'name': self.name,
            'active': self.active,
            'isolated': self.isolated,
            'users': [user.user.json() for user in self.users],
            'campaign': [self.campaign.cid if minimal else self.campaign.json(True)]
        }
