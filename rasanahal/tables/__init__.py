# Imports go here!
from .campaign import Campaign
from .character import Character
from .class_ import Class
from .classassociation import ClassAssociation
from .group import Group
from .groupassociation import GroupAssociation
from .message import Message
from .object_ import Object
from .objectassociation import ObjectAssociation
from .partecipantassociation import PartecipantAssociation
from .race import Race
from .skill import Skill
from .skillassociation import SkillAssociation
from .spell import Spell
from .spellassociation import SpellAssociation

# Enter the tables of your Pack here!
available_tables = [
    Campaign,
    Character,
    Class,
    ClassAssociation,
    Group,
    GroupAssociation,
    Message,
    Object,
    ObjectAssociation,
    PartecipantAssociation,
    Race,
    Skill,
    SkillAssociation,
    Spell,
    SpellAssociation,
]

# Don't change this, it should automatically generate __all__
__all__ = [table.__name__ for table in available_tables]
