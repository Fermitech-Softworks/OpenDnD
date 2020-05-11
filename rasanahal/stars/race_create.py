import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Race


class RaceCreateStar(rca.ApiStar):
    summary = "Method that creates an object."
    description = """Given the name of the race and a basic description, 
    this method creates a new race."""
    methods = ["POST"]
    path = "/api/race/create"
    requires_auth = True
    parameters = {
        "name": "The name of the race.",
        "desc": "The description of the race."
    }
    tags = ["race"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        RacT = self.alchemy.get(Race)
        new_race: Race = RacT(
            name=data['name'],
            desc=data['desc']
        )
        data.session.add(new_race)
        data.session.commit()
        return {"race": new_race.json(True)}
