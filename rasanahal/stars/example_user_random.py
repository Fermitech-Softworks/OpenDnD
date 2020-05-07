import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae

import random
from royalnet.backpack.tables import User


class UserRandomStar(rca.ApiStar):
    summary = "Un metodo di esempio per far vedere come si usa sqlalchemy con Constellation."

    description = """Questo metodo restituisce i dati di un utente casuale."""

    methods = ["GET"]

    path = "/api/example/user/random/v1"

    requires_auth = False

    parameters = {}

    tags = ["example"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        # Tutte le tabelle devono passare prima attraverso self.alchemy.get per come è fatto sqlalchemy
        UserT = self.alchemy.get(User)

        # Faccio una query che restituisca tutti gli utenti
        users = data.session.query(UserT).all()

        if len(users) == 0:
            raise Exception("Non ci sono utenti registrati.")

        user = random.sample(users)[0]

        return user.json()
