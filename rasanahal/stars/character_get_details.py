import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Character


class CharacterGetDetailsStar(rca.ApiStar):
    summary = "Method that returns the character data."
    description = """Given a character identifier, it returns the json string that represents the character."""
    methods = ["GET"]
    path = "/api/character/get_details"
    requires_auth = True
    tags = ["character"]

    parameters = {
        'cid': "The character's id."
    }

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        CharT = self.alchemy.get(Character)
        char = data.session.query(CharT).filter_by(cid=data['cid']).first()
        if "admin" not in user.roles and char.owner_id!=user.uid:
            raise Exception("You don't belong to this roleplay demiplane.")
        return {"campaign": char.json(False)}