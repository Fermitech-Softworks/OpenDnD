import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Spell


class SpellCreateStar(rca.ApiStar):
    summary = "Method that creates a spell."
    description = """Given the name of the spell, the school, the components and the die, 
    this method creates a new spell."""
    methods = ["POST"]
    path = "/api/spell/create"
    requires_auth = True
    parameters = {
        "name": "The name of the spell.",
        "school": "The school of the spell",
        "comp": "The components.",
        "die": "The die (e.g. 1d10+COS)"
    }
    tags = ["spell"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        SpeT = self.alchemy.get(Spell)
        new_spell: Spell = SpeT(
            name=data['name'],
            school=data['school'],
            comp=data['comp'],
            die=data['die']
        )
        data.session.add(new_spell)
        data.session.commit()
        return {"spell": new_spell.json(True)}
