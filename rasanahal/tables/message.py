from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declared_attr


class Message:
    __tablename__ = 'message'

    @declared_attr
    def mid(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def text(self):
        return Column(String, nullable=False)

    @declared_attr
    def time(self):
        return Column(DateTime, nullable=False)

    @declared_attr
    def group_id(self):
        return Column(Integer, ForeignKey('group.gid'))

    @declared_attr
    def group(self):
        return relationship("Group", back_populates="messages")

    @declared_attr
    def owner_id(self):
        return Column(Integer, ForeignKey('users.uid'))

    @declared_attr
    def owner(self):
        return relationship("User", backref="messages")

    def json(self, minimal):
        return {
            'id': self.mid,
            'text': self.text,
            'time': self.time,
            'group': [self.owner.uid if minimal else self.owner.json()],
            'user': [self.group.group_id if minimal else self.group.json(True)]
        }
