import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Character


class UserGetCharStar(rca.ApiStar):
    summary = "Method that returns all the characters of a certain user."
    description = """This method returns all data concerning a user's character."""
    methods = ["GET"]
    path = "/api/user/get_characters"
    requires_auth = True
    tags = ["user"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        CharT = self.alchemy.get(Character)
        chars = data.session.query(CharT).filter_by(user_id=user.uid).order_by(CharT.name).all()
        return {"character": c.json(True) for c in chars}
