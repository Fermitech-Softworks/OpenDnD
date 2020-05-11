import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Class


class ClassCreateStar(rca.ApiStar):
    summary = "Method that creates a class."
    description = """Given the name of the race and a basic description, 
    this method creates a new race."""
    methods = ["POST"]
    path = "/api/race/create"
    requires_auth = True
    parameters = {
        "name": "The name of the class.",
        "desc": "The description of the class."
    }
    tags = ["class"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        ClaT = self.alchemy.get(Class)
        new_class: Class = ClaT(
            name=data['name'],
            desc=data['desc']
        )
        data.session.add(new_class)
        data.session.commit()
        return {"class": new_class.json(True)}
