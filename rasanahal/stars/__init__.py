# Imports go here!
from .example_echo import EchoStar
from .example_user_random import UserRandomStar
from .campaign_add_user import CampaignAddUserStar
from .campaign_create import CampaignCreateStar
from .user_get_campaign import UserGetCampaignsStar
from .user_get import UserGetStar
from .user_create import UserCreateStar
from .user_get_characters import UserGetCharStar
from .character_add_class import CharacterAddClassStar
from .character_add_object import CharacterAddObjectStar
from .character_add_skill import CharacterAddSkillStar
from .character_add_spell import CharacterAddSpellStar
from .character_create import CharacterCreateStar
from .group_create import GroupCreateStar
from .group_add_user import GroupAddUserStar
from .group_get import GroupGetStar
from .character_get_details import CharacterGetDetailsStar
from .campaign_get_details import CampaignGetDetailsStar


# Enter the PageStars of your Pack here!
available_page_stars = [
    EchoStar,
    UserRandomStar,
    UserGetCampaignsStar,
    CampaignCreateStar,
    CampaignAddUserStar,
    CampaignGetDetailsStar,
    UserGetStar,
    UserCreateStar,
    UserGetCharStar,
    CharacterAddClassStar,
    CharacterAddObjectStar,
    CharacterAddSkillStar,
    CharacterAddSpellStar,
    CharacterCreateStar,
    CharacterGetDetailsStar,
    GroupGetStar,
    GroupCreateStar,
    GroupAddUserStar,

]


# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_page_stars]
