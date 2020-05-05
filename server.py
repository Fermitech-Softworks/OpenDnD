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


class SkillAssociation(Base):
    __tablename__ = 'skillassociation'
    skill_id = Column(Integer, ForeignKey('skill.sid'), primary_key=True)
    character_id = Column(Integer, ForeignKey('character.cid'), primary_key=True)
    level = Column(Integer, nullable=False)
    skill = relationship("Skill", back_populates="characters")
    character = relationship("Character", back_populates="skills")


class GroupAssociation(Base):
    __tablename__ = 'groupassociation'
    user_id = Column(Integer, ForeignKey('user.uid'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.gid'), primary_key=True)
    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="users")


class PartecipantAssociation(Base):
    __tablename__ = 'partecipantassociation'
    user_id = Column(Integer, ForeignKey('user.uid'), primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaign.cid'), primary_key=True)
    is_gm = Column(Boolean, nullable=False, default=False)
    user = relationship("User", back_populates='partecipations')
    campaign = relationship("Campaign", back_populates='players')


class ClassAssociation(Base):
    __tablename__ = 'classassociation'
    character_id = Column(Integer, ForeignKey('character.cid'), primary_key=True)
    class_id = Column(Integer, ForeignKey('class.cid'), primary_key=True)
    level = Column(Integer, nullable=False)
    character = relationship("Character", back_populates="classes")
    Class = relationship("Class", back_populates="characters")


class ObjectAssociation(Base):
    __tablename__ = 'objectassociation'
    character_id = Column(Integer, ForeignKey('character.cid'), primary_key=True)
    object_id = Column(Integer, ForeignKey('object.oid'), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)
    character = relationship("Character", back_populates="inventory")
    object = relationship("Object", back_populates="characters")


class SpellAssociation(Base):
    __tablename__ = 'spellassociation'
    character_id = Column(Integer, ForeignKey('character.cid'), primary_key=True)
    spell_id = Column(Integer, ForeignKey('spell.sid'), primary_key=True)
    character = relationship("Character", back_populates="spells")
    spell = relationship("Spell", back_populates="characters")


class User(Base):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    username = Column(String, nullable=False)
    partecipations = relationship("PartecipantAssociation", back_populates='user')
    characters = relationship("Character", back_populates="owner")
    groups = relationship("GroupAssociation", back_populates='user')
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
    players = relationship("PartecipantAssociation", back_populates='campaign')
    groups = relationship("Group", back_populates="campaigns")
    characters = relationship("Character", back_populates="campaign")

    def __repr__(self):
        return "CAMPAIGN - {} {}".format(self.cid, self.title)


class Group(Base):
    __tablename__ = 'group'
    gid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    campaign_id = Column(Integer, ForeignKey('campaign.cid'))
    campaigns = relationship("Campaign", back_populates="groups")
    active = Column(Boolean, nullable=False)
    isolated = Column(Boolean, nullable=False)
    users = relationship("GroupAssociation", back_populates='group')
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


class Skill(Base):
    __tablename__ = 'skill'
    sid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    attribute = Column(Integer, nullable=False)  # 1:STR, 2:DEX, 3:COS, 4:INT, 6:CHA, 7:WIS
    desc = Column(String, nullable=True)
    characters = relationship("SkillAssociation", back_populates="skill")


class Character(Base):
    __tablename__ = 'character'
    cid = Column(Integer, primary_key=True)
    isNpc = Column(Boolean, nullable=False)
    # Basic information
    name = Column(String, nullable=False)
    race_id = Column(Integer, ForeignKey('race.rid'))
    race = relationship("Race", back_populates="characters")
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
    # Misc
    notes = Column(String, nullable=True)
    # Connections with other tables
    owner_id = Column(Integer, ForeignKey('user.uid'))
    owner = relationship("User", back_populates="characters")
    campaign_id = Column(Integer, ForeignKey('campaign.cid'))
    campaign = relationship("Campaign", back_populates="characters")
    skills = relationship("SkillAssociation", back_populates="character")
    inventory = relationship("ObjectAssociation", back_populates="character")
    classes = relationship("ClassAssociation", back_populates="character")
    spells = relationship("SpellAssociation", back_populates="character")


class Class(Base):
    __tablename__ = 'class'
    cid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    desc = Column(String, nullable=False)
    characters = relationship("ClassAssociation", back_populates='Class')


class Object(Base):
    __tablename__ = 'object'
    oid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    cost = Column(String)
    desc = Column(String, nullable=False)
    characters = relationship("ObjectAssociation", back_populates='object')


class Race(Base):
    __tablename__ = 'race'
    rid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    desc = Column(String, nullable=False)
    characters = relationship("Character", back_populates="race")


class Spell(Base):
    __tablename__ = 'spell'
    sid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    school = Column(String, nullable=False)
    comp = Column(String, nullable=False)
    die = Column(String)
    characters = relationship("SpellAssociation", back_populates='spell')


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
        if token.creation.day == datetime.datetime.now().day and (
                token.creation.hour - datetime.datetime.now().hour) < 6:
            return True
        dbs.delete(token)
        dbs.commit()
    return False


def check_auth(usertoken):
    uid = verify_token(usertoken)
    if uid < 0:
        abort(403)
    return uid


def create_header(data):
    return JSONResponse(data, headers={"Access-Control-Allow-Origin": "*"})


def verify_dm(uid, cid):
    if dbs.query(PartecipantAssociation).filter_by(user_id=uid, campaign_id=cid, is_gm=True).first() is not None:
        return True
    return False


async def api_get_token(request):
    form = await request.form()
    if login(form['email'], form['password']):
        user = locate_player(form['email'])
        token = dbs.query(Token).filter_by(owner_id=user.email).first()
        test = False
        if token:
            test = verify_token(token.token, user.uid)
            token.creation = datetime.datetime.now()
            dbs.commit()
        if not token or not test:
            token = Token(user.email)
            dbs.add(token)
            dbs.commit()
        return JSONResponse({'result': 'success', 'token': token.token, 'username': user.username, 'uid': user.uid},
                            headers={"Access-Control-Allow-Origin": "*"})
    else:
        return JSONResponse({'result': 'failure', 'desc': 'Invalid username or password'},
                            headers={"Access-Control-Allow-Origin": "*"})


async def api_create_user(request):
    form = await request.form()
    try:
        p = bytes(form["password"], encoding="utf-8")
        ash = bcrypt.hashpw(p, bcrypt.gensalt())
        newuser = User(email=form['email'], password=ash, username=form['username'])
        dbs.add(newuser)
        dbs.commit()
    except IntegrityError:
        return JSONResponse({'result': 'failure', 'desc': 'User already exists.'},
                            headers={"Access-Control-Allow-Origin": "*"})
    return JSONResponse({'result': 'success'}, headers={"Access-Control-Allow-Origin": "*"})


async def api_get_campaigns(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'},
                            headers={"Access-Control-Allow-Origin": "*"})
    campaigns = dbs.query(Campaign).join(User).filter_by(uid=form['uid']).all()
    response = {'result': 'success',
                'campaigns': [{'title': None, 'owner': {'uid': None, 'username': None}, 'cid': None}]}
    a = 0
    for campaign in campaigns:
        response['campaigns'][a]['title'] = campaign.title
        response['campaigns'][a]['owner']['uid'] = campaign.owner_id
        owner = locate_player_uid(campaign.owner_id)
        response['campaigns'][a]['owner']['username'] = owner.username
        response['campaigns'][a]['cid'] = campaign.cid
        a += 1
    return JSONResponse(response, headers={"Access-Control-Allow-Origin": "*"})


async def api_create_campaign(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'})
    newcampaign = Campaign(title=form['title'])
    dbs.add(newcampaign)
    dmassoc = PartecipantAssociation(user_id=form['uid'], campaign_id=newcampaign.cid, is_gm=True)
    dbs.add(dmassoc)
    dbs.commit()
    return JSONResponse({'result': 'success', 'desc': 'Your campaign has been saved'},
                        headers={"Access-Control-Allow-Origin": "*"})


async def api_create_campaign_association(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'})
    if verify_dm(form['uid'], form['cid']):
        newconnection = PartecipantAssociation(user_id=form['target-uid'], campaign_id=form['cid'], is_gm=False)
        dbs.add(newconnection)
        dbs.commit()
        return JSONResponse(
            {'result': 'success', 'desc': 'Your changes have been saved.'},
            headers={"Access-Control-Allow-Origin": "*"})
    return JSONResponse(
        {'result': 'failure', 'desc': 'You are either not authorized or something ended in the shadow-realm.'},
        headers={"Access-Control-Allow-Origin": "*"})


async def api_delete_campaign_association(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'})
    if not verify_dm(form['uid'], form['cid']):
        return JSONResponse(
            {'result': 'failure', 'desc': 'You are either not authorized or something ended in the shadow-realm.'},
            headers={"Access-Control-Allow-Origin": "*"})
    conn = dbs.query(PartecipantAssociation).filter_by(user_id=form['uid'], campaign_id=form['cid']).first()
    if not conn:
        return JSONResponse(
            {'result': 'failure', 'desc': 'You are either not authorized or something ended in the shadow-realm.'},
            headers={"Access-Control-Allow-Origin": "*"})
    dbs.delete(conn)
    dbs.commit()
    return JSONResponse(
        {'result': 'success', 'desc': 'Your changes have been saved.'},
        headers={"Access-Control-Allow-Origin": "*"})


async def api_create_group(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'})
    if not verify_dm(form['uid'], form['cid']):
        return JSONResponse(
            {'result': 'failure', 'desc': 'You are either not authorized or something ended in the shadow-realm.'},
            headers={"Access-Control-Allow-Origin": "*"})
    newgroup = Group(name=form['name'], campaign_id=form['cid'], active=False, isolated=False)
    dbs.add(newgroup)
    newassoc = GroupAssociation(user_id=form['uid'], group_id=newgroup.gid)
    dbs.add(newassoc)
    dbs.commit()
    return JSONResponse(
        {'result': 'success', 'desc': 'Your group has been saved.'},
        headers={"Access-Control-Allow-Origin": "*"})


async def api_get_groups(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'})
    groups = dbs.query(User).join(Group).filter_by(uid=form['uid'], campaign_id=form['cid']).all()
    if not groups:
        return JSONResponse(
            {'result': 'failure', 'desc': 'You are either not authorized or something ended in the shadow-realm.'},
            headers={"Access-Control-Allow-Origin": "*"})
    response = {'result': 'success', 'groups': [{'gid': None, 'title': None}]}
    a = 0
    for group in groups:
        response['groups'][a]['gid'] = group.gid
        response['groups'][a]['title'] = group.title
        a += 1
    return JSONResponse(response, headers={"Access-Control-Allow-Origin": "*"})


async def api_get_group_members(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'})
    auth = dbs.query(GroupAssociation).filter_by(user_id=form['uid'], group_id=form['gid']).first()
    if not auth:
        return JSONResponse(
            {'result': 'failure', 'desc': 'You are either not authorized or something ended in the shadow-realm.'},
            headers={"Access-Control-Allow-Origin": "*"})
    users = dbs.query(GroupAssociation).join(User).filter_by(group_id=form['gid']).all()
    response = {'result': 'success', 'users': [{'uid': None, 'username': None}]}
    if not auth:
        return JSONResponse(
            {'result': 'failure', 'desc': 'You are either not authorized or something ended in the shadow-realm.'},
            headers={"Access-Control-Allow-Origin": "*"})
    a = 0
    for user in users:
        response['users'][a]['uid'] = user.uid
        response['users'][a]['username'] = user.username
        a += 1
    return JSONResponse(response, headers={"Access-Control-Allow-Origin": "*"})



async def api_get_characters(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'},
                            headers={"Access-Control-Allow-Origin": "*"})
    characters = dbs.query(Character).join(User).filter_by(uid=form['uid']).all()
    print(len(characters))
    response = {'result': 'success', 'characters': [{'cid': None, 'name': None, 'race': None, 'level': None}]}
    a = 0
    for character in characters:
        response['characters'][a]['cid'] = character.cid
        response['characters'][a]['name'] = character.name
        response['characters'][a]['race'] = character.race
        response['characters'][a]['level'] = character.level
        a += 1
    print(response)
    return JSONResponse(response, headers={"Access-Control-Allow-Origin": "*"})


async def api_get_character_details(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'},
                            headers={"Access-Control-Allow-Origin": "*"})
    character = dbs.query(Character).Join(User).Join(Skill).Join(Race).Join(Object).join(Spell).join(Class).filter_by(
        cid=form['cid']).first()
    if character:
        skills = []
        for skill in character.skills:
            skills[skill.sid]['name'] = skill.name
            skills[skill.sid]['attrib'] = skill.attribute
            skills[skill.sid]['desc'] = skill.desc
        response = {'result': 'success',
                    'character': {'cid': character.cid, 'isNpc': character.isNpc, 'name': character.name,
                                  'race': character.race, 'level': character.level, 'maxhp': character.maxhp,
                                  'currenthp': character.currenthp, 'proficiency': character.proficiency,
                                  'strenght': character.strenght, 'dexterity': character.dexterity,
                                  'constitution': character.constitution, 'intelligence': character.intelligence,
                                  'wisdom': character.wisdom, 'charisma': character.charisma, 'notes': character.notes,
                                  'skills': skills},
                    'owner': {'uid': character.owner.uid, 'username': character.owner.username}}
        return JSONResponse(response, headers={"Access-Control-Allow-Origin": "*"})
    return JSONResponse(
        {'result': 'failure', 'desc': 'Not found'},
        headers={"Access-Control-Allow-Origin": "*"})


async def api_create_character(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'},
                            headers={"Access-Control-Allow-Origin": "*"})
    user = locate_player_uid(form['uid'])
    race = dbs.query(Race).filter_by(name=form['race']).first
    newchar = Character(isNpc=form['isNpc'], name=form['name'], level=form['level'], race_id=race.id,
                        maxhp=form['maxhp'], currenthp=form['currenthp'], proficiency=form['proficiency'],
                        strenght=form['strenght'], dexterity=form['dexterity'], constitution=form['constitution'],
                        intelligence=form['intelligence'], wisdom=form['wisdom'], charisma=form['charisma'],
                        strenght_st=form['strenght_st'], dexterity_st=form['dexterity_st'],
                        constitution_st=form['constitution_st'], intelligence_st=form['intelligence_st'],
                        wisdom_st=form['wisdom_st'], charisma_st=form['charisma_st'], notes=form['notes'],
                        owner_id=user.uid)
    dbs.add(newchar)
    for skill in form['skills']:
        newconn = SkillAssociation(skill_id=skill['sid'], character_id=newchar.cid, level=skill['level'])
        dbs.add(newconn)
    for cle in form['classes']:
        newconn = ClassAssociation(class_id=cle['cid'], character_id=newchar.cid, level=cle['level'])
        dbs.add(newconn)
    for spell in form['spells']:
        newconn = SpellAssociation(spell_id=spell['sid'], character_id=newchar.cid)
        dbs.add(newconn)
    for obj in form['inventory']:
        newconn = ObjectAssociation(object_id=obj['oid'], character_id=newchar.cid, quantity=obj['qty'])
        dbs.add(newconn)
    dbs.commit()
    return JSONResponse({'result': 'success', 'desc': 'Your character has been saved.'},
                        headers={"Access-Control-Allow-Origin": "*"})


async def api_get_skills(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'},
                            headers={"Access-Control-Allow-Origin": "*"})
    skills = dbs.query(Skill).all()
    response = {'result': 'success', 'skills': [{'sid': None, 'name': None, 'attribute': None, 'desc': None}]}
    a = 0
    for skill in skills:
        response['skills'][a]['sid'] = skill.sid
        response['skills'][a]['name'] = skill.name
        response['skills'][a]['attribute'] = skill.attribute
        response['skills'][a]['desc'] = skill.desc
        a += 1
    return JSONResponse(response, headers={"Access-Control-Allow-Origin": "*"})


async def api_get_skills_details(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'},
                            headers={"Access-Control-Allow-Origin": "*"})
    skill = dbs.query(Skill).filter_by(sid=form['sid']).first()
    if skill:
        return JSONResponse(
            {'result': 'success',
             'skill': {'sid': skill.sid, 'name': skill.name, 'attribute': skill.attribute, 'desc': skill.desc}},
            headers={"Access-Control-Allow-Origin": "*"})
    return JSONResponse(
        {'result': 'failure', 'desc': 'Not found'},
        headers={"Access-Control-Allow-Origin": "*"})


async def api_get_objects(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'},
                            headers={"Access-Control-Allow-Origin": "*"})
    objects = dbs.query(Object).all()
    response = {'result': 'success', 'objects': [{'oid': None, 'name': None, 'cost': None, 'desc': None}]}
    a = 0
    for obj in objects:
        response['objects'][a]['oid'] = obj.oid
        response['objects'][a]['name'] = obj.name
        response['objects'][a]['cost'] = obj.cost
        response['objects'][a]['desc'] = obj.desc
        a += 1
    return JSONResponse(response, headers={"Access-Control-Allow-Origin": "*"})


async def api_get_object_details(request):
    form = await request.form()
    if not verify_token(form['token'], form['uid']):
        return JSONResponse({'result': 'failure', 'desc': 'You may be not logged in or your token has expired.'},
                            headers={"Access-Control-Allow-Origin": "*"})
    obj = dbs.query(Skill).filter_by(sid=form['sid']).first()
    if obj:
        return JSONResponse(
            {'result': 'success', 'skill': {'oid': obj.oid, 'name': obj.name, 'cost': obj.cost, 'desc': obj.desc}},
            headers={"Access-Control-Allow-Origin": "*"})
    return JSONResponse(
        {'result': 'failure', 'desc': 'Not found'},
        headers={"Access-Control-Allow-Origin": "*"})


async def test(request):
    return JSONResponse({'result': 'success', 'desc': 'The server is up.'},
                        headers={"Access-Control-Allow-Origin": "*"})


log.info("Now creating the Rasanhal WebApp Object...")
app = Starlette(debug=True, routes=[
    Route('/test', test, methods=['POST', 'GET']),
    Route('/api/login', api_get_token, methods=['POST']),
    Route('/api/register', api_create_user, methods=['POST']),
    Route('/api/get_campaigns', api_get_campaigns, methods=['POST']),
    Route('/api/get_characters', api_get_characters, methods=['POST']),
    Route('/api/get_characters_details', api_get_characters, methods=['POST']),
    Route('/api/create_character', api_get_characters, methods=['POST']),
    Route('/api/get_skills', api_get_skills, methods=['POST'])])

log.info("Rasanahal WebApp ready.")
