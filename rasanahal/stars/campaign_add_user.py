import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import PartecipantAssociation, Campaign


class CampaignAddUserStar(rca.ApiStar):
    summary = "Method that adds a user to a campaign."
    description = """Given both the ids of the campaign and the user, it adds the player to che choosen.
    campaign. It can also be specified if the user has to be added as GM."""
    methods = ["POST"]
    path = "/api/campaigns/add_user"
    requires_auth = True
    parameters = {
        "uid": "The user id",
        "cid": "The campaign id",
        "as_gm": "True if the new player must be added as GM."
    }
    tags = ["user"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        ParT = self.alchemy.get(PartecipantAssociation)
        CamT = self.alchemy.get(Campaign)
        new_assoc: PartecipantAssociation = ParT(
            user_id=data['uid'],
            campaign_id=data['cid'],
            is_gm=data['as_gm']
        )
        data.session.add(new_assoc)
        data.session.commit()
        campaign = data.session.query(CamT).filter_by(cid=data['cid']).first()
        return {"campaign": campaign.json(True)}
