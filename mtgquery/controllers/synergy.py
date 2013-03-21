from datetime import datetime
from ..lib.alchemy_extensions import get_last_n
from ..lib.parsers import card_group, synergy_group
from ..models import (
    DBSession,
    InvalidDataException,
)
from ..models.card import Card
from ..models.synergy import (
    Synergy,
    SynergyCard,
    SynergyText
)


class SynergyHashNotFoundException(Exception):
    def __init__(self, hash):
        self.hash = hash

    @property
    def msg(self):
        return "Could not find the hash \"{}\"".format(self.hash)


import re
MAX_ENTRIES = 40
MAX_DESCRIPTION_LINES = 40
MAX_DESCRIPTION_LINE_LENGTH = 500
SYNERGY_TEXT_REGEX = re.compile(r"^((?P<count>\d+)\s)?(#(?P<text>.+?))$")
CARD_REGEX = re.compile(r"^((?P<count>\d+)\s)?(?P<card>[^:]+)\s*(:\s*(?P<set>.*))?$")


def get_custom_text(string):
    string = string.strip()
    match = SYNERGY_TEXT_REGEX.search(string)
    if not match:
        return None

    count = match.group('count')
    if count:
        count = count.strip()
    count = int(count) if count else 1

    text = match.group('text')
    if text:
        text = text.strip()

    return count, text


def get_card_and_set(string, notifications=None):
        string = string.strip()
        match = CARD_REGEX.search(string)
        if not match:
            return None

        count = match.group('count')
        if count:
            count = count.strip()
        count = int(count) if count else 1

        card = match.group('card')
        if card:
            card = card.strip()

        set = match.group('set')
        if set:
            set = set.strip()

        return card, count, set


def nb_lines(string):
    string = string.replace(u"\r\n", u"\n")
    lines = string.split(u"\n")
    return filter(nonblank, lines)


def nonblank(line):
    return len(line.strip()) > 0


def create_synergy(cards, title, description):
    '''returns the hash that the submitted synergy can be found at'''
    notifications = []

    synergy = Synergy(create_date=datetime.now(), title=title, view_count=0, visible=True)
    synergy.random_generate_unique()
    DBSession.add(synergy)

    description = description.replace(u"\r\n", u"\n")
    description_lines = description.split(u"\n")

    if len(description_lines) > MAX_DESCRIPTION_LINES:
        synergy.visible = False
        description_lines = description_lines[:MAX_ENTRIES]
        #ADD A MESSAGE ABOUT TRUNCATED CONTENT
        #"Description truncated: maximum of {} lines"

    notified = False
    for i, line in enumerate(description_lines):
        if len(line) > MAX_DESCRIPTION_LINE_LENGTH:
            synergy.visible = False
            description_lines[i] = line[:MAX_DESCRIPTION_LINE_LENGTH]
            if not notified:
                notified = True
                #ADD A MESSAGE ABOUT TRUNCATED CONTENT
                #"Entry truncated: maximum of {} cards/text"

    description = u'\n'.join(description_lines)
    synergy.description = description

    entry_lines = nb_lines(cards)
    if len(entry_lines) > MAX_ENTRIES:
        synergy.visible = False
        entry_lines = entry_lines[:MAX_ENTRIES]
        #ADD A MESSAGE ABOUT TRUNCATED CONTENT

    for index, line in enumerate(entry_lines):
        custom_text = get_custom_text(line)
        if custom_text:
            count, text = custom_text
            synergy_text = SynergyText(synergy=synergy, text=text, index=index, quantity=count)
            DBSession.add(synergy_text)
        else:
            card_and_set = get_card_and_set(line)
            if card_and_set:
                card_name, count, set = card_and_set
                try:
                    card = Card.interpolate_name_and_set(card_name, set)
                    synergy_card = SynergyCard(synergy=synergy, card=card, index=index, quantity=count)
                    DBSession.add(synergy_card)
                except InvalidDataException as e:
                    #LOG THE MESSAGE FOR THEM
                    synergy.visible = False
                    print e
            else:
                #Not synergy text, not card.  Log invalid format
                #LOG MESSAGE ABOUT INVALID FORMAT
                synergy.visible = False

    return synergy.hash, notifications


def load_synergy(hash):
    synergy = DBSession.query(Synergy).filter_by(hash=hash).first()
    if synergy is None:
        raise SynergyHashNotFoundException(hash)

    #Update view count
    synergy.view_count += 1
    DBSession.add(synergy)

    synergy_cards = synergy.cards
    synergy_texts = synergy.texts

    #Generate urls and counts
    entries = []
    url_base = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={mvid}&type=card'

    for sc in synergy_cards:
        url = url_base.format(mvid=sc.card.multiverse_id)
        entries.append((sc.index, sc.quantity, url))
    for st in synergy_texts:
        url = 'http://res.cloudinary.com/mtg-query/image/upload/card_back.jpg'
        text = st.text
        url = text, url  # Packed data for synergy_raw
        entries.append((st.index, st.quantity, url))
    entries.sort()
    counts = [e[1] for e in entries]
    urls = [e[2] for e in entries]

    title = synergy.title
    description = synergy.description

    card_list = card_group.to_list(synergy_cards)
    text_list = synergy_group.to_list(synergy_texts)
    lists = card_list + text_list
    lists.sort()
    form_cards_text = "\n".join([L[1] for L in lists])
    form_dict = {
        'form_cards_text': form_cards_text,
        'form_title': title,
        'form_description': description
    }
    return urls, counts, title, description, form_dict


def get_random_hash():
    return Synergy.get_random_hash()


def get_newest_synergyies():
    n = 10
    data = []
    synergies = get_last_n(DBSession, Synergy, n, 'id', ['cards', 'texts'])
    for synergy in synergies:
        title = synergy.title if len(synergy.title) > 0 else "(Untitled)"
        data.append({
            'title': title,
            'length': len(synergy.cards) + len(synergy.texts),
            'url': '/s/{}'.format(synergy.hash)
        })
    return data
