from datetime import datetime
from ..lib.alchemy_extensions import get_last_n
from sqlalchemy.orm import joinedload_all
from ..models import (
    DBSession,
    InvalidDataException,
)
from ..models.synergy import (
    Synergy,
    SynergyCard,
    SynergyText
)

newest_synergies_len = 10
newest_synergies = []

MAX_ENTRIES = 40
MAX_DESCRIPTION_LENGTH = 10000  # Limit is number of characters pre-formatting


def preheat_cache():
    print "preheating newest synergies"
    get_newest_synergyies()


def get_newest_synergyies():
    if len(newest_synergies) < newest_synergies_len:
        # Load some more from the DB
        n = newest_synergies_len - len(newest_synergies)
        additional_synergies = get_last_n(DBSession, Synergy, n, u'id', [u'cards', u'texts'], visible=True)
        map(cache_new_synergy, additional_synergies)
    return list(newest_synergies)


def cache_new_synergy(synergy):
    global newest_synergies
    title = synergy.title if len(synergy.title) > 0 else u"(Untitled)"
    synergy_data = {
        'title': title,
        'length': len(synergy.cards) + len(synergy.texts),
        'url': u'/s/{}'.format(synergy.hash)
    }
    newest_synergies.append(synergy_data)
    if len(newest_synergies) > newest_synergies_len:
        newest_synergies = newest_synergies[-newest_synergies_len:]


class SynergyHashNotFoundException(Exception):
    def __init__(self, hash):
        self.hash = hash

    @property
    def msg(self):
        return u"Could not find the hash \"{}\"".format(self.hash)


def nb_lines(string):
    string = string.replace(u"\r\n", u"\n")
    lines = string.split(u"\n")
    nonblank = lambda line: len(line.strip()) > 0
    return filter(nonblank, lines)


def create_synergy(cards, title, description):
    '''returns the hash that the submitted synergy can be found at'''

    synergy = Synergy(create_date=datetime.now(), title=title, view_count=0, visible=True)
    synergy.random_generate_unique()
    DBSession.add(synergy)
    notifications = []

    if not title:
        notifications.append(u"Synergy not indexed: Must provide a title")
        synergy.visible = False

    description = description.replace(u"\r\n", u"\n")
    if len(description) > MAX_DESCRIPTION_LENGTH:
        description = description[:MAX_DESCRIPTION_LENGTH]
        notifications.append(u"Description truncated: Exceeded {} characters".format(MAX_DESCRIPTION_LENGTH))

    synergy.description = description

    entry_lines = nb_lines(cards)
    if len(entry_lines) > MAX_ENTRIES:
        entry_lines = entry_lines[:MAX_ENTRIES]
        notifications.append(u"Cards truncated: Exceeded {} cards".format(MAX_ENTRIES))

    for index, line in enumerate(entry_lines):
        try:
            synergy_text = SynergyText.from_string(line)
            synergy_text.synergy = synergy
            synergy_text.index = index
            DBSession.add(synergy_text)
        except InvalidDataException:
            # If it isn't a synergy text, it's either a card or invalid
            try:
                synergy_card = SynergyCard.from_string(line)
                synergy_card.synergy = synergy
                synergy_card.index = index
                DBSession.add(synergy_card)
            except InvalidDataException as e:  # as e:
                notifications.append(u"Invalid line \"{}\": {}".format(line, e.msg))
    if len(synergy.cards) == len(synergy.texts) == 0:
        notifications.append(u"Synergy not indexed: Must have at least one card (or custom text card)")
        synergy.visible = False

    if synergy.visible:
        cache_new_synergy(synergy)
    return synergy.hash, notifications


def load_synergy(hash):
    synergy = DBSession.query(Synergy).options(
        joinedload_all(Synergy.cards),
        joinedload_all(Synergy.texts)
    ).filter_by(hash=hash).first()
    if synergy is None:
        raise SynergyHashNotFoundException(hash)

    #Update view count
    synergy.view_count += 1
    DBSession.add(synergy)

    synergy_cards = synergy.cards
    synergy_texts = synergy.texts

    #Generate urls and counts
    entries = []
    url_base = u'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={mvid}&type=card'

    for sc in synergy_cards:
        url = url_base.format(mvid=sc.card.multiverse_id)
        entries.append((sc.index, sc.quantity, url))
    for st in synergy_texts:
        url = u'http://res.cloudinary.com/mtg-query/image/upload/card_back.jpg'
        text = st.text
        url = text, url  # Packed data for synergy_raw
        entries.append((st.index, st.quantity, url))
    entries.sort()
    counts = [e[1] for e in entries]
    urls = [e[2] for e in entries]

    title = synergy.title
    description = synergy.description

    indexed = [(i.index, i) for i in synergy_cards + synergy_texts]
    indexed.sort()
    form_cards_text = u"\n".join(unicode(item) for index, item in indexed)
    form_dict = {
        'form_cards_text': form_cards_text,
        'form_title': title,
        'form_description': description
    }
    return urls, counts, title, description, form_dict


def get_random_hash():
    return Synergy.get_random_hash()
