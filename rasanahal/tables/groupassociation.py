from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class GroupAssociation:
    __tablename__ = 'groupassociation'

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey('users.uid'), primary_key=True)

    @declared_attr
    def group_id(self):
        return Column(Integer, ForeignKey('group.gid'), primary_key=True)

    @declared_attr
    def user(self):
        return relationship("User", backref="groups")

    @declared_attr
    def group(self):
        return relationship("Group", back_populates="users")
