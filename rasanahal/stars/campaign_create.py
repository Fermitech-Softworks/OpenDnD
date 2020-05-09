import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Campaign, PartecipantAssociation


class CampaignCreateStar(rca.ApiStar):
    summary = "Method that creates a campaign."
    description = """Given the title of the campaign, it creates the campaign and
    the association with the dungeon master (the user that creates the campaign).
    """
    methods = ["POST"]
    path = "/api/campaigns/create"
    requires_auth = True
    parameters = {
        "title": "The title of the campaign"
    }
    tags = ["user"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        CampaignT = self.alchemy.get(Campaign)
        ParT = self.alchemy.get(PartecipantAssociation)
        new_camp: Campaign = CampaignT(
            title=data['title']
        )
        dm_assoc: PartecipantAssociation = ParT(
            user_id=user.uid,
            campaign_id=new_camp,
            is_gm=True
        )
        data.session.add(new_camp)
        data.session.add(dm_assoc)
        data.session.commit()
        return {"campaign": new_camp.json()}
