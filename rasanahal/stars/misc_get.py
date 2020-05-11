import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Object, Race, Class, Skill, Spell


class MiscGetStar(rca.ApiStar):
    summary = "Method that gives the list of items that belong to a certain class."
    description = """Method that gives the list of items that belong to a certain class."""
    methods = ["GET"]
    path = "/api/misc/get"
    requires_auth = True
    parameters = {
        "mode": "A string among obj, race, class, skill, spell."
    }
    tags = ["skill", "class", "object", "race", "spell"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        if data['mode'] not in ["obj", "race", "class", "skill", "spell"]:
            raise Exception("Please provide a valid mode value.")
        elif data['mode'] == "obj":
            ObjT = self.alchemy.get(Object)
            result = data.session.query(ObjT).order_by(ObjT.name).all()
        elif data['mode'] == "race":
            RacT = self.alchemy.get(Race)
            result = data.session.query(RacT).order_by(RacT.name).all()
        elif data['mode'] == "class":
            ClaT = self.alchemy.get(Class)
            result = data.session.query(ClaT).order_by(ClaT.name).all()
        elif data['mode'] == "skill":
            SkiT = self.alchemy.get(Skill)
            result = data.session.query(SkiT).order_by(SkiT.name).all()
        else:
            SpeT = self.alchemy.get(Spell)
            result = data.session.query(SpeT).order_by(SpeT.name).all()
        return {data['mode']: r.json(True) for r in result}
