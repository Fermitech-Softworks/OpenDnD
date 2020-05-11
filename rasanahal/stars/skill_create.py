import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Skill


class SkillCreateStar(rca.ApiStar):
    summary = "Method that creates a skill."
    description = """Given the name of the race, the attribute and a basic description, 
    this method creates a new skill."""
    methods = ["POST"]
    path = "/api/skill/create"
    requires_auth = True
    parameters = {
        "name": "The name of the skill.",
        "attrib": "Number that defines the attribute. 1:STR, 2:DEX, 3:COS, 4:INT, 6:CHA, 7:WIS.",
        "desc": "The description of the skill."
    }
    tags = ["skill"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        if data['attrib'] not in [1, 2, 3, 4, 5, 6]:
            raise Exception("Please provide a valid attrib value.")
        SkiT = self.alchemy.get(Skill)
        new_skill: Skill = SkiT(
            name=data['name'],
            attribute=data['attrib'],
            desc=data['desc']
        )
        data.session.add(new_skill)
        data.session.commit()
        return {"skill": new_skill.json(True)}
