import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Character, Class, ClassAssociation


class CharacterAddClassStar(rca.ApiStar):
    summary = "Method that adds a class to the character."
    description = """Given the character id and the class id, it creates an entry in the ClassAssociation table, that
    also contains the character's level in that class"""
    methods = ["POST"]
    path = "/api/character/add_class"
    requires_auth = True
    parameters = {
        "cid": "The character id.",
        "clid": "The class id.",
        "level": "The level."
    }
    tags = ["character"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        CharT = self.alchemy.get(Character)
        ClassT = self.alchemy.get(Class)
        CasT = self.alchemy.get(ClassAssociation)
        character = data.session.query(CharT).filter_by(cid=data['cid']).first()
        if user.uid != character.owner_id:
            raise Exception("You are not the owner of this character.")
        if data['level'] > 20 and data['level'] < 1:
            raise Exception("Please provide a valid level.")
        test = data.session.query(CasT).filter_by(character_id=data['cid'], class_id=data['sid']).first()
        if test is None:
            new_assoc: ClassAssociation = CasT(
                class_id=data['sid'],
                character_id=data['cid'],
                level=data['level']
            )
            data.session.add(new_assoc)
        else:
            test.level = data['level']
        total = 0
        for associations in character.skills:
            total += associations.level
        character.level = total
        data.session.commit()
        return {"character": character.json(True)}
