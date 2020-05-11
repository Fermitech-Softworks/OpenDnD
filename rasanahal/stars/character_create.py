import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Character


class CharacterCreateStar(rca.ApiStar):
    summary = "Method that creates a character."
    description = """ Given the parameters, it creates a character connected to the user that calls the method.
    """
    methods = ["POST"]
    path = "/api/character/create"
    requires_auth = True
    parameters = {
        'is_npc': "Boolean, true if npc.",
        'name': "Name of the character.",
        'race_id': "Id of the character's race.",
        "level": "Character's level.",
        "maxhp": "Number of maximum hitpoints.",
        "currenthp": "Number of current hitpoints.",
        "proficiency": "Value of the proficiency stat.",
        "strength": "Value of the strenght stat.",
        "dexterity": "Value of the dexterity stat.",
        "constitution": "Value of the constitution stat.",
        "intelligence": "Value of the intelligence stat.",
        "wisdom": "Value of the wisdom stat.",
        "charisma": "Value of the charisma stat.",
        "strenght_st": "Boolean, true if character has proficiency with the stat's saving throw",
        "dexterity_st": "Boolean, true if character has proficiency with the stat's saving throw",
        "constitution_st": "Boolean, true if character has proficiency with the stat's saving throw",
        "intelligence_st": "Boolean, true if character has proficiency with the stat's saving throw",
        "wisdom_st": "Boolean, true if character has proficiency with the stat's saving throw",
        "charisma_st": "Boolean, true if character has proficiency with the stat's saving throw",
        "notes": "Character notes."
    }
    tags = ["character"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        CharT = self.alchemy.get(Character)
        new_char: Character = CharT(
            is_npc=data['is_npc'],
            name=data['name'],
            race_id=data['race_id'],
            level=data['level'],
            maxhp=data['maxhp'],
            currenthp=data['currenthp'],
            proficiency=data['proficiency'],
            strength=data['strength'],
            dexterity=data['dexterity'],
            constitution=data['constitution'],
            intelligence=data['intelligence'],
            wisdom=data['wisdom'],
            charisma=data['charisma'],
            strength_st=data['strength_st'],
            dexterity_st=data['dexterity_st'],
            constitution_st=data['constitution_st'],
            intelligence_st=data['intelligence_st'],
            wisdom_st=data['wisdom_st'],
            charisma_st=data['charisma_st'],
            notes=data['charisma_st'],
            owner_id=user.uid
        )
        data.session.ad(new_char)
        data.session.commit()
        return {"character": new_char.json(True)}
