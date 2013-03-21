import re
import transaction
from datetime import datetime
from mtgquery.lib.alchemy_extensions import has_model as _has_model
from mtgquery.util import get_logger
from mtgquery.models import DBSession
from ..models.card import Card
from ..models.synergy import (
    Synergy,
    SynergyCard,
    SynergyText
)

log = get_logger(__name__)

synergies = [
    [
        "Xi2PK",
        "mill ALL the things",
        "Now where did I put my [[Oxidize]]...",
        "1 Painter's Servant : Shadowmoor",
        "1 Grindstone : Tempest"
    ],
    [
        "WyXa4",
        "Lots and lots of lots",
        """(Works best with Arcum Dagsson fetching required pieces)
Fetch Mirrorworks with Arcum Dagsson

Fetch Sculpting Steel, copy Mirrorworks.  Original Mirrorworks triggers on Steel etb, pay 2 to create a token of Mirrorworks (you now have 3 Mirrorworks in play)

Target 1 Mirrorworks with Karn, Silver Golem.  Cast Clone, choosing the Mirrorworks that karn targeted.

All 3 Mirrorworks trigger on Clone etb, pay 6 and put 3 tokens of (the cloned) Mirrorworks into play (you now have 7 Mirrorworks in play)

Fetch Gauntlet of Power.  7 copied of the Mirrorworks trigger go on the stack.  Respond to each one so that you can tap lands for 1, then 2, then 3, then 4, then 5, then 6, then 7, then 8 mana per land.

You can now play something like Staff of Nin or Defense Grid (or both!) and copy it 7 times.  With defense grid, counterspell costs 23 mana and with Staff of Nin, you draw 8 cards each turn (and with 4 lands, you have 32 mana available)

Your next step is to get Memnarch out and make all your lands artifacts, so that you can use Clock of Omens to untap them.  Now every artifact you control basically reads: {tap} Add {u}{U}{u}{u} to your mana pool.  Which you can use to make more permanents into artifacts, to untap the lands even more....
        """,
        "1 Arcum Dagsson : Coldsnap",
        "1 Mirrorworks : Mirrodin Besieged",
        "1 Sculpting Steel : Tenth Edition",
        "1 Karn, Silver Golem : From the Vault: Relics",
        "1 Clone : Magic 2013",
        "1 Gauntlet of Power : Time Spiral"
    ],
    [
        "JYhaz",
        "Immediate Planeswalker Ultimate",
        """Doubling Season doubles the number of counters that would be placed on permanents you control.

When Tamiyo comes into play, she gets 8 loyalty counters instead of 4.

Yay Synergy!""",
        "1 Doubling Season : Ravnica: City of Guilds",
        "1 Tamiyo, the Moon Sage : Avacyn Restored"
    ],
    [
        "onYy4",
        "Immediate Planeswalker Ultimate",
        """Doubling Season doubles the number of counters that would be placed on permanents you control.

When your planeswalker comes into play, it gets twice its starting loyalty (and can probably use its ultimate immediately.)

Yay Synergy!""",
        "1 Doubling Season : Ravnica: City of Guilds",
        "1 #Any Planeswalker"
    ],
    [
        "asEAk",
        "Burn",
        """You only really need 1 extra elf.

**But who doesn't want more elves.**""",
        "1 Wirewood Channeler : Legions",
        "2 #Any elf",
        "1 Pemmin's Aura : Scourge",
        "1 #Any X burn spell"
    ]
]

text_regex = re.compile(r"^((?P<count>\d+)\s)?(#(?P<text>.+?))$")
card_regex = re.compile(r"^((?P<count>\d+)\s)?(?P<card>[^:]+)\s*(:\s*(?P<set>.*))?$")


def load_synergy(session, hash, title, description, *cards):
    has_model = lambda model, **kw: _has_model(session, model, **kw)
    if has_model(Synergy, hash=hash):
        log.info("Skipping help file synergy creation for hash {}: hash already defined.".format(hash))
        return
    synergy = Synergy(hash=hash, create_date=datetime.now(), title=title, description=description, view_count=0, is_public=True)
    for i, card in enumerate(cards):
        text_match = text_regex.search(card)
        card_match = card_regex.search(card)
        if text_match:
            count = text_match.group('count')
            if count:
                count = count.strip()
            count = int(count) if count else 1

            text = text_match.group('text')
            if text:
                text = text.strip()

            synergy_text = SynergyText(synergy=synergy, text=text, index=i, quantity=count)
            session.add(synergy_text)
        elif card_match:
            count = card_match.group('count')
            if count:
                count = count.strip()
            count = int(count) if count else 1

            card = card_match.group('card')
            if card:
                card = card.strip()

            set = card_match.group('set')
            if set:
                set = set.strip()

            card = Card.interpolate_name_and_set(card, set)

            synergy_card = SynergyCard(synergy=synergy, card=card, index=i, quantity=count)
            session.add(synergy_card)
    log.info("Generated help file synergy for hash {}".format(hash))


def main():
    session = DBSession()
    map(lambda s: load_synergy(session, *s), synergies)
    transaction.commit()
