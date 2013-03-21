from mtgquery.lib.synergy.load_synergy import load_existing_synergy
from mtgquery.lib.synergy.query import random_hash, newest_synergies
from datetime import datetime
from ..lib.util.rate_limiting_generator import line_generator, rate_limit
from ..lib.notifications import GenericNotification
from ..lib.parsers import (
    cardcount_generator,
    synergytext_generator,
    synergy_text_regex
)
from ..models import (
    DBSession,

    Card,
    Synergy,
    SynergyCard,
    SynergyText
)


def create_synergy(cards, title, description):
    '''returns the hash that the submitted synergy can be found at'''

    notifications = []

    #Cut down our description to max lines
    desc_gen = line_generator(description, False)
    desc_limit = 10
    desc_valid = lambda line: len(line.strip()) > 0
    exceeded_fmt = "Description truncated: maximum of {} non-blank lines"
    desc_on_limit = lambda (i, limit, value): notifications.append(GenericNotification(exceeded_fmt.format(desc_limit)))
    desc_rate_gen = rate_limit(desc_gen, desc_limit, desc_valid, desc_on_limit)
    description = u'\n'.join(desc_rate_gen)

    #Cut down our cards to max lines
    card_gen = line_generator(cards, False)
    card_limit = 40
    card_valid = lambda line: len(line.strip()) > 0
    exceeded_fmt = "Cards truncated: maximum of {} cards/text"
    card_on_limit = lambda (i, limit, value): notifications.append(GenericNotification(exceeded_fmt.format(card_limit)))
    card_rate_gen = rate_limit(card_gen, card_limit, card_valid, card_on_limit)
    cards = '\n'.join(card_rate_gen)

    synergy = Synergy(create_date=datetime.now(), title=title, description=description, view_count=0, visible=True)
    # For now we're using random generation, since the number of collisions over the 600mil+ possible values is... low.
    #synergy.generate_hash()
    synergy.random_generate_unique()
    DBSession.add(synergy)

    re_ignores = [synergy_text_regex]
    for card_name, count, set, index in cardcount_generator(cards, notifications=notifications, re_ignores=re_ignores):
        card = Card.interpolate_name_and_set(card_name, set, notifications=notifications)
        if card is None:
            continue

        synergy_card = SynergyCard(synergy=synergy, card=card, index=index, quantity=count)
        DBSession.add(synergy_card)

    for text, count, index in synergytext_generator(cards, notifications=notifications):
        synergy_text = SynergyText(synergy=synergy, text=text, index=index, quantity=count)
        DBSession.add(synergy_text)

    return synergy.hash, notifications


def load_synergy(hash):
    view_count, urls, counts, title, description, form_dict = load_existing_synergy(hash)
    return urls, counts, title, description, form_dict


def get_random_hash():
    return random_hash()


def get_newest_synergyies():
    return newest_synergies(10)
