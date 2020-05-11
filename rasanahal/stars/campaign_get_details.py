import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Campaign, PartecipantAssociation


class CampaignGetDetailsStar(rca.ApiStar):
    summary = "Method that returns the campaign data."
    description = """Given a campaigns identifier, it returns the json string that represents the campaign."""
    methods = ["GET"]
    path = "/api/campaign/get_details"
    requires_auth = True
    tags = ["campaign"]

    parameters = {
        'cid': "The campaign's id."
    }

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        CampaignT = self.alchemy.get(Campaign)
        ParT = self.alchemy.get(PartecipantAssociation)
        if "admin" not in user.roles and data.session.query(ParT).filter_by(user_id=user.uid, campaign_id=data['cid']).first() is None:
            raise Exception("You don't belong to this roleplay demiplane.")
        campaign = data.session.query(CampaignT).filter_by(cid=data['cid']).first()
        return {"campaign": campaign.json(False)}
