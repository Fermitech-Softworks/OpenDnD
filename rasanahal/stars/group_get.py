import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Group, GroupAssociation


class GroupGetStar(rca.ApiStar):
    summary = "Method that returns all the users inside a Group."
    description = """Given the id of the group, it returns the details of the group itself."""
    methods = ["GET"]
    path = "/api/group/get"
    requires_auth = True
    parameters = {
        "gid": "The group id"
    }
    tags = ["group"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        GroT = self.alchemy.get(Group)
        AssT = self.alchemy.get(GroupAssociation)
        if data.session.query(AssT).filter_by(group_id=data['gid'], user_id=user.uid).first() is None:
            raise Exception("You are not in this campaign.")
        group = data.session.query(GroT).filter_by(gid=data['gid']).first()
        return {"group": group.json(False)}
