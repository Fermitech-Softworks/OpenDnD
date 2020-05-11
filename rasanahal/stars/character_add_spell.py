import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae
from royalnet.backpack.tables import User
from rasanahal.tables import Character, Spell, SpellAssociation


class CharacterAddSpellStar(rca.ApiStar):
    summary = "Method that adds a spell to the character."
    description = """Given the character id and the spell id, it creates an entry in the SpellAssociation table."""
    methods = ["POST"]
    path = "/api/character/add_spell"
    requires_auth = True
    parameters = {
        "cid": "The character id.",
        "sid": "The spell id.",
    }
    tags = ["character"]

    async def api(self, data: rca.ApiData) -> ru.JSON:
        user = await data.user()
        CharT = self.alchemy.get(Character)
        SpellT = self.alchemy.get(Spell)
        SasT = self.alchemy.get(SpellAssociation)
        character = data.session.query(CharT).filter_by(cid=data['cid']).first()
        if user.uid != character.owner_id:
            raise Exception("You are not the owner of this character.")
        test = data.session.query(SasT).filter_by(character_id=data['cid'], spell_id=data['sid']).first()
        if test is None:
            new_assoc: SpellAssociation = SasT(
                spell_id=data['sid'],
                character_id=data['cid'],
            )
            data.session.add(new_assoc)
            data.session.commit()
        return {"character": character.json(True)}
