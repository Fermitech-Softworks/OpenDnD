import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Object, Race, Class, Skill, Spell


class MiscGetDetailsStar(rca.ApiStar):
    summary = "Method that gives the details of something minor."
    description = """Given the identifier of an entity among Objects, Races, Classes, Skills and Spells, it returns
    the details."""
    methods = ["GET"]
    path = "/api/misc/get_details"
    requires_auth = True
    parameters = {
        "id": "The identifier.",
        "mode": "A string among obj, race, class, skill, spell."
    }
    tags = ["skill", "class", "object", "race", "spell"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        if data['mode'] not in ["obj", "race", "class", "skill", "spell"]:
            raise Exception("Please provide a valid mode value.")
        elif data['mode'] == "obj":
            ObjT = self.alchemy.get(Object)
            result = data.session.query(ObjT).filter_by(oid=data['id']).first()
        elif data['mode'] == "race":
            RacT = self.alchemy.get(Race)
            result = data.session.query(RacT).filter_by(rid=data['id']).first()
        elif data['mode'] == "class":
            ClaT = self.alchemy.get(Class)
            result = data.session.query(ClaT).filter_by(cid=data['id']).first()
        elif data['mode'] == "skill":
            SkiT = self.alchemy.get(Skill)
            result = data.session.query(SkiT).filter_by(sid=data['id']).first()
        else:
            SpeT = self.alchemy.get(Spell)
            result = data.session.query(SpeT).filter_by(sid=data['id']).first()
        return {data['mode']: result.json(True)}
