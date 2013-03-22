from datetime import datetime
from ..lib.alchemy_extensions import get_last_n
from ..models import (
    DBSession,
    InvalidDataException,
)
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
        return u"Could not find the hash \"{}\"".format(self.hash)


MAX_ENTRIES = 40
MAX_DESCRIPTION_LINES = 40
MAX_DESCRIPTION_LINE_LENGTH = 500


def nb_lines(string):
    string = string.replace(u"\r\n", u"\n")
    lines = string.split(u"\n")
    return filter(nonblank, lines)


def nonblank(line):
    return len(line.strip()) > 0


def create_synergy(cards, title, description):
    '''returns the hash that the submitted synergy can be found at'''

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
        try:
            synergy_text = SynergyText.from_string(line)
            synergy_text.synergy = synergy
            synergy_text.index = index
            DBSession.add(synergy_text)
        except InvalidDataException as e:
            try:
                synergy_card = SynergyCard.from_string(line)
                synergy_card.synergy = synergy
                synergy_card.index = index
                DBSession.add(synergy_card)
            except InvalidDataException as e:
                synergy.visible = False
                print e
    return synergy.hash


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


def get_newest_synergyies():
    n = 10
    data = []
    synergies = get_last_n(DBSession, Synergy, n, u'id', [u'cards', u'texts'])
    for synergy in synergies:
        title = synergy.title if len(synergy.title) > 0 else u"(Untitled)"
        data.append({
            'title': title,
            'length': len(synergy.cards) + len(synergy.texts),
            'url': u'/s/{}'.format(synergy.hash)
        })
    return data
