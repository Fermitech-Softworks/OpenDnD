import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Group, GroupAssociation, PartecipantAssociation


class GroupAddUserStar(rca.ApiStar):
    summary = "Method that adds a user to the group."
    description = """Given the id of the group and of the target user, it adds the user to the group."""
    methods = ["POST"]
    path = "/api/group/add_user"
    requires_auth = True
    parameters = {
        "gid": "The group id",
        "uid": "The user id"
    }
    tags = ["group"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        GroT = self.alchemy.get(Group)
        AssT = self.alchemy.get(GroupAssociation)
        ParT = self.alchemy.get(PartecipantAssociation)
        group = data.session.query(GroT).filter_by(gid=data['gid']).first()
        if user.uid != group.campaign.locate_gm():
            raise Exception("You are not the game master.")
        if data.session.query(ParT).filter_by(campaign_id=group.campaign_id, user_id=data['uid']).first() is None:
            raise Exception("The user does not belong to this plane of roleplay.")
        new_assoc: GroupAssociation = AssT(
            user_id=data['uid'],
            group_id=data['gid']
        )
        data.session.add(new_assoc)
        data.session.commit()
        return {"group": group.json(True)}
