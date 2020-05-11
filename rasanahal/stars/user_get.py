import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User


class UserGetStar(rca.ApiStar):
    summary = "Method that returns user data."
    description = """Given a user identifier, it returns the json string that represents the selected entity."""
    methods = ["GET"]
    path = "/api/user/get"
    requires_auth = True
    parameters = {
        "uid": "User's id",
    }
    tags = ["user"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        UserT = self.alchemy.get(User)
        target = data.session.query(UserT).filter_by(uid=user.uid).first()
        return {"user": target.json(False)}
