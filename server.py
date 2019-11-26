import binascii
import datetime

import bcrypt
from sqlalchemy.orm import sessionmaker, relationship
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.routing import Route
from starlette.config import Config
from starlette.routing import Route
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, LargeBinary, Boolean, \
    ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
import logging
# Alright then,
import secrets

config = Config('.env')
engine = create_engine('sqlite:///database.sqlite')
templates = Jinja2Templates(directory='templates')
meta = MetaData()
Base = declarative_base()

log = logging.getLogger(__name__)

partecipant = Table('partecipant', Base.metadata,
                    Column('uid', Integer, ForeignKey('user.uid')),
                    Column('cid', Integer, ForeignKey('campaign.cid'))
                    )

groupconnection = Table('groupconnection', Base.metadata,
                        Column('uid', Integer, ForeignKey('user.uid')),
                        Column('gid', Integer, ForeignKey('group.gid')))


class User(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    username = Column(String, nullable=False)
    owned_campaigns = relationship("Campaign", back_populates="owner")
    partecipations = relationship("Campaign", secondary=partecipant, back_populates='players')
    characters = relationship("Character", back_populates="owner")
    groups = relationship("Group", secondary=groupconnection, back_populates='users')
    messages = relationship("Message", back_populates="owner")
    tokens = relationship("Token", back_populates="owner")

    def __repr__(self):
        return "USER - {} {} {}".format(self.uid, self.email, self.username)


class Token(Base):
    __tablename__ = "token"
    tid = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('user.uid'))
    creation = Column(DateTime, nullable=False)
    owner = relationship("User", back_populates="tokens")

    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.creation = datetime.datetime.now()
        self.token = secrets.token_hex(16)


class Campaign(Base):
    __tablename__ = 'campaign'
    cid = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('user.uid'))
    owner = relationship("User", back_populates="owned_campaigns")
    players = relationship("User", secondary=partecipant, back_populates='partecipations')
    chats = relationship("Chat", back_populates="campaign")
    characters = relationship("Character", back_populates="campaign")

    def __repr__(self):
        return "CAMPAIGN - {} {} {}".format(self.cid, self.title, self.owner_id)


class Chat(Base):
    __tablename__ = 'chat'
    cid = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaign.cid'))
    campaign = relationship("Campaign", back_populates="chats")
    groups = relationship("Group", back_populates="chat")

    def __repr__(self):
        return "CHAT - {} {}".format(self.cid, self.campaign_id)


class Group(Base):
    __tablename__ = 'group'
    gid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    chat_id = Column(Integer, ForeignKey('chat.cid'))
    chat = relationship("Chat", back_populates="groups")
    active = Column(Boolean, nullable=False)
    isolated = Column(Boolean, nullable=False)
    users = relationship("User", secondary=groupconnection, back_populates='groups')
    messages = relationship("Message", back_populates="group")

    def __repr__(self):
        return "GROUP - {} {} {}".format(self.gid, self.name, self.chat_id)


class Message(Base):
    __tablename__ = 'message'
    mid = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    group_id = Column(Integer, ForeignKey('group.gid'))
    group = relationship("Group", back_populates="messages")
    owner_id = Column(Integer, ForeignKey('user.uid'))
    owner = relationship("User", back_populates="messages")

    def __repr__(self):
        return "MESSAGE - {} {} {}".format(self.mid, self.group_id, self.owner_id)


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


log.info("Now checking db structures...")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
dbs = Session()
conn = engine.connect()
log.info("Database ready and connected.")


async def abort(code):
    raise HTTPException(code, detail=None)


def locate_player(email):
    return dbs.query(User).filter_by(email=email).first()


def locate_player_uid(uid):
    return dbs.query(User).filter_by(uid=uid).first()


def login(email, password):
    user = locate_player(email)
    try:
        return bcrypt.checkpw(bytes(password, encoding="utf-8"), user.password)
    except AttributeError:
        # Se non esiste l'Utente
        return False


def verify_token(usertoken, uid):
    user = locate_player_uid(uid)
    token = dbs.query(Token).filter_by(token=usertoken, owner_id=user.email).first()
    print(token)
    if token:
        if token.creation.day == datetime.datetime.now().day and (token.creation.hour - datetime.datetime.now().hour) < 6:
            return True
        dbs.remove(token)
        dbs.commit()
    return False


def check_auth(usertoken):
    uid = verify_token(usertoken)
    if uid < 0:
        abort(403)
    return uid


async def api_get_token(request):
    form = await request.form()
    if login(form['email'], form['password']):
        user = locate_player(form['email'])
        token = Token(user.email)
        dbs.add(token)
        dbs.commit()
        return JSONResponse({'result': 'success', 'token': token.token, 'username': user.username, 'uid': user.uid})
    else:
        return JSONResponse({'result': 'failure', 'desc': 'Invalid username or password'})


async def api_create_user(request):
    form = await request.form()
    try:
        p = bytes(form["password"], encoding="utf-8")
        ash = bcrypt.hashpw(p, bcrypt.gensalt())
        newuser = User(email=form['email'], password=ash, username=form['username'])
        dbs.add(newuser)
        dbs.commit()
    except IntegrityError:
        return JSONResponse({'result': 'failure', 'desc': 'User already exists.'})
    return JSONResponse({'result': 'success'})


async def api_get_campaigns(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'})
    campaigns = dbs.query(Campaign).join(User).filter_by(uid=form['uid']).all()
    response = {'result': 'success', 'campaigns': {}}
    for campaign in campaigns:
        response['campaigns']['title'] = campaign.title
        response['campaigns']['owner']['uid'] = campaign.owner_id
        owner = locate_player_uid(campaign.owner_id)
        response['campaigns']['owner']['username'] = owner.username
    return JSONResponse(response)


async def test(request):
    return templates.TemplateResponse('main.htm', {'request': request})


log.info("Now creating the Rasanhal WebApp Object...")
app = Starlette(debug=True, routes=[
    Route('/test', test, methods=['POST', 'GET']),
    Route('/api/login', api_get_token, methods=['POST']),
    Route('/api/register', api_create_user, methods=['POST']),
    Route('/api/get_campaigns', api_get_campaigns, methods=['POST']),
    Mount("/scripts", app=StaticFiles(directory='scripts'), name="scripts")], )

log.info("Rasanahal WebApp ready.")
