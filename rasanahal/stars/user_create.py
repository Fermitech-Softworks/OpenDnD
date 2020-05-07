import royalnet.constellation.api as rca
import royalnet.utils as ru

from royalnet.backpack.tables import User
from sqlalchemy.exc import IntegrityError
import re


username_regex = re.compile(r"""^[a-z]+$""")
email_regex = re.compile(r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")


class UserCreateStar(rca.ApiStar):
    summary = "Create a new Rasanahal user."

    description = ""

    methods = ["GET"]

    path = "/api/user/create/v1"

    requires_auth = False

    parameters = {}

    tags = ["user"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        UserT = self.alchemy.get(User)

        # Assicuriamoci che l'username inserito sia valido
        if not username_regex.match(data["username"]):
            raise Exception("This username is invalid.")

        # Assicuriamoci che l'email inserita sia valida
        if not email_regex.match(data["email"]):
            raise Exception("This email is invalid.")

        # Assicuriamoci che non ci siano utenti con lo stesso username
        user_with_same_username = data.session.query(UserT).filter_by(username=data["username"]).first()
        if user_with_same_username is not None:
            raise Exception("This username is already in use.")

        # Assicuriamoci che non ci siano utenti con la stessa email
        user_with_same_email = data.session.query(UserT).filter_by(email=data["email"]).first()
        if user_with_same_email is not None:
            raise Exception("This email is already in use.")

        # Assicuriamoci che non ci siano utenti con la stessa password
        # jk lol

        # Magari aggiungiamo jcaptcha e controlliamo che sia valido?
        # Uno spammerino di utenti potrebbe essere problematico

        new_user: User = UserT(
            username=data["username"],
            email=data["email"]
        )
        new_user.set_password(data["password"])

        data.session.add(new_user)
        data.session.commit()

        # Restituiamo i dati del nuovo utente creato perchè potrebbero essere comodi nel frontend
        return new_user.json()
