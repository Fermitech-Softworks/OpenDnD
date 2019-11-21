from sqlalchemy.orm import sessionmaker, relationship
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from starlette.routing import Route
from starlette.config import Config
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, LargeBinary, Boolean, \
    ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
import logging

config = Config('.env')
engine = create_engine('sqlite:///database.sqlite')
templates = Jinja2Templates(directory='templates')
meta = MetaData()
Base = declarative_base()


class Participant(Base):
    __tablename__ = 'partecipant'
    pid = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("user.uid"))
    campaign = Column(Integer, ForeignKey("campaign.cid"))


class GroupConnection(Base):
    __tablename__ = 'groupconnection'
    gid = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("user.uid"))
    group = Column(Integer, ForeignKey("group.gid"))


class User(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    username = Column(String, nullable=False)
    owned_campaigns = relationship("Campaign", back_populates="owner")
    partecipations = relationship("Campaign", secondary=Participant, back_populates='players')
    characters = relationship("Character", back_populates="owner")
    groups = relationship("Group", secondary=GroupConnection, back_populates='users')
    messages = relationship("Message", back_populates="owner")


class Campaign(Base):
    __tablename__ = 'campaign'
    cid = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('user.uid'))
    owner = relationship("User", back_populates="owned_campaigns")
    players = relationship("User", secondary=Participant, back_populates='partecipations')
    chats = relationship("Chat", back_populates="campaign")
    characters = relationship("Characters", back_populates="campaign")


class Chat(Base):
    __tablename__ = 'chat'
    cid = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaign.cid'))
    campaign = relationship("Campaign", back_populates="chats")
    groups = relationship("Group", back_populates="chat")


class Group(Base):
    __tablename__ = 'group'
    gid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    chat_id = Column(Integer, ForeignKey('chat.cid'))
    chat = relationship("Chat", back_populates="groups")
    active = Column(Boolean, nullable=False)
    isolated = Column(Boolean, nullable=False)
    users = relationship("User", secondary=GroupConnection, back_populates='groups')
    messages = relationship("Message", back_populates="group")


class Message(Base):
    __tablename__ = 'message'
    mid = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    group_id = Column(Integer, ForeignKey('group.gid'))
    group = relationship("Group", back_populates="messages")
    owner_id = Column(Integer, ForeignKey('user.uid'))
    owner = relationship("User", back_populates="messages")


class Character(Base):
    __tablename__ = 'character'
    cid = Column(Integer, primary_key=True)
    isNpc = Column(Boolean, nullable=False)
    # Basic information
    name = Column(String, nullable=False)
    race = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    maxhp = Column(Integer, nullable=False)
    currenthp = Column(Integer, nullable=False)
    proficiency = Column(Integer, nullable=False)
    # Stats
    strenght = Column(Integer, nullable=False)
    dexterity = Column(Integer, nullable=False)
    constitution = Column(Integer, nullable=False)
    intelligence = Column(Integer, nullable=False)
    wisdom = Column(Integer, nullable=False)
    charisma = Column(Integer, nullable=False)
    # Saving throws
    strenght_st = Column(Boolean, nullable=False)
    dexterity_st = Column(Boolean, nullable=False)
    constitution_st = Column(Boolean, nullable=False)
    intelligence_st = Column(Boolean, nullable=False)
    wisdom_st = Column(Boolean, nullable=False)
    charisma_st = Column(Boolean, nullable=False)
    # Skills
    acrobatics = Column(Integer, nullable=False)
    animal = Column(Integer, nullable=False)
    arcana = Column(Integer, nullable=False)
    athelics = Column(Integer, nullable=False)
    deception = Column(Integer, nullable=False)
    history = Column(Integer, nullable=False)
    insight = Column(Integer, nullable=False)
    intimidation = Column(Integer, nullable=False)
    investigation = Column(Integer, nullable=False)
    medicine = Column(Integer, nullable=False)
    nature = Column(Integer, nullable=False)
    perception = Column(Integer, nullable=False)
    performance = Column(Integer, nullable=False)
    persuasion = Column(Integer, nullable=False)
    religion = Column(Integer, nullable=False)
    hand = Column(Integer, nullable=False)
    stealth = Column(Integer, nullable=False)
    survival = Column(Integer, nullable=False)
    # Misc
    notes = Column(String, nullable=True)
    # Connections with other tables
    owner_id = Column(Integer, ForeignKey('user.uid'))
    owner = relationship("User", back_populates="characters")
    campaign_id = Column(Integer, ForeignKey('campaign.cid'))
    campaign = relationship("Campaign", back_populates="characters")


logging.info("Now checking db structures...")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
dbs = Session()
conn = engine.connect()
logging.info("Database ready and connected.")


async def homepage(request):
    return JSONResponse({'hello': 'world'})


async def test(request):
    return templates.TemplateResponse('test.htm', {'request': request, 'messaggio1': 'ciao', 'messaggio2': 'mondo'})


logging.info("Now starting the Rasanahal Server...")
app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/test', test)])
logging.info("Rasanahal Server started.")
