import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Group, GroupAssociation


class GroupCreateStar(rca.ApiStar):
    summary = "Method that creates a new group within a campaign."
    description = """Given both the ids of the campaign and the name of the group, it creates the group that contains
    the GM."""
    methods = ["POST"]
    path = "/api/group/create"
    requires_auth = True
    parameters = {
        "cid": "The campaign id",
        "name": "The group name"
    }
    tags = ["group"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        GroT = self.alchemy.get(Group)
        AssT = self.alchemy.get(GroupAssociation)
        new_group: Group = GroT(
            name=data['name'],
            campaign_id=data['cid']
        )
        if user.uid != new_group.campaign.locate_gm():
            raise Exception("You are not the game master.")
        data.session.add(new_group)
        dm_assoc: GroupAssociation = AssT(
            user_id=user.uid,
            group_id=new_group.gid
        )
        data.session.commit()
        return {"group": new_group.json(True)}
