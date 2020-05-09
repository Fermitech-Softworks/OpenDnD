import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Campaign, PartecipantAssociation


class CampaignGetStar(rca.ApiStar):
    summary = "Method that returns the campaigns data."
    description = """Given a user identifier, it returns the json string that represents the campaigns in which he partecipates."""
    methods = ["POST"]
    path = "/api/campaigns/get"
    requires_auth = True
    parameters = {
        "extended": "If true, additional information will be shown."
    }
    tags = ["user"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        CampaignT = self.alchemy.get(Campaign)
        ParT = self.alchemy.get(PartecipantAssociation)
        campaigns = data.session.query(CampaignT).Join(ParT).filter_by(ParT.user_id == user.uid).all()
        return {"user": c.json(True) for c in campaigns}
