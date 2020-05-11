import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Object


class ObjectCreateStar(rca.ApiStar):
    summary = "Method that creates an object."
    description = """Given the name of the object, its cost and a basic description, 
    this method creates a new object."""
    methods = ["POST"]
    path = "/api/object/create"
    requires_auth = True
    parameters = {
        "name": "The name of the object.",
        "cost": "The cost of the object (e.g. 10GP).",
        "desc": "The description of the object."
    }
    tags = ["object"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        ObjT = self.alchemy.get(Object)
        new_obj: Object = ObjT(
            name=data['name'],
            cost=data['cost'],
            desc=data['desc']
        )
        data.session.add(new_obj)
        data.session.commit()
        return {"object": new_obj.json(True)}
