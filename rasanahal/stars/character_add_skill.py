import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Character, Skill, SkillAssociation


class CharacterAddSkillStar(rca.ApiStar):
    summary = "Method that adds a skill to the character."
    description = """Given the character id and the skill id, it creates an entry in the SkillAssociation table, that
    also contains the user defined level of proficiency"""
    methods = ["POST"]
    path = "/api/character/add_skill"
    requires_auth = True
    parameters = {
        "cid": "The character id.",
        "sid": "The skill id.",
        "level": "The proficiency level."
    }
    tags = ["character", "skill"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        CharT = self.alchemy.get(Character)
        SkillT = self.alchemy.get(Skill)
        SasT = self.alchemy.get(SkillAssociation)
        character = data.session.query(CharT).filter_by(cid=data['cid']).first()
        if user.uid != character.owner_id:
            raise Exception("You are not the owner of this character.")
        if data['level'] not in [0, 1, 2]:
            raise Exception("Please provide a valid proficiency level.")
        test = data.session.query(SasT).filter_by(character_id=data['cid'], skill_id=data['sid']).first()
        if test is None:
            new_assoc: SkillAssociation = SasT(
                skill_id=data['sid'],
                character_id=data['cid'],
                level=data['level']
            )
            data.session.add(new_assoc)
        else:
            test.level = data['level']
        data.session.commit()
        return {"character": character.json(True)}
