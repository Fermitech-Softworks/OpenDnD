# Imports go here!
from .example_echo import EchoStar
from .example_user_random import UserRandomStar

# Enter the PageStars of your Pack here!
available_page_stars = [
    EchoStar,
    UserRandomStar,
]


# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_page_stars]
