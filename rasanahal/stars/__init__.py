# Imports go here!
from .example_echo import EchoStar
from .example_user_random import UserRandomStar
from .campaign_add_user import CampaignAddUserStar
from .campaign_create import CampaignCreateStar
from .campaign_get import CampaignGetStar
from .user_get import UserGetStar

# Enter the PageStars of your Pack here!
available_page_stars = [
    EchoStar,
    UserRandomStar,
    CampaignGetStar,
    CampaignCreateStar,
    CampaignAddUserStar,
    UserGetStar
]


# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_page_stars]
