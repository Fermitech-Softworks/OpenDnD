import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Character, Object, ObjectAssociation


class CharacterAddObjectStar(rca.ApiStar):
    summary = "Method that adds an object to the character."
    description = """Given the character id and the skill id, it creates an entry in the SkillAssociation table, that
    also contains the user defined level of proficiency"""
    methods = ["POST"]
    path = "/api/character/add_object"
    requires_auth = True
    parameters = {
        "cid": "The character id.",
        "oid": "The object id.",
        "quantity": "The quantity of a certain object."
    }
    tags = ["character"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        CharT = self.alchemy.get(Character)
        ObjT = self.alchemy.get(Object)
        OasT = self.alchemy.get(ObjectAssociation)
        character = data.session.query(CharT).filter_by(cid=data['cid']).first()
        if user.uid != character.owner_id:
            raise Exception("You are not the owner of this character.")
        if data['level'] < 0:
            raise Exception("Please provide a valid quantity.")
        test = data.session.query(OasT).filter_by(character_id=data['cid'], object_id=data['sid']).first()
        if test is None:
            new_assoc: ObjectAssociation = OasT(
                object_id=data['sid'],
                character_id=data['cid'],
                quantity=data['quantity']
            )
            data.session.add(new_assoc)
        else:
            if data['quantity'] == 0:
                data.session.remove(test)
            else:
                test.level = data['level']
        data.session.commit()
        return {"character": character.json(True)}
