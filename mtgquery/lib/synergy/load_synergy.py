from ..exceptions import SynergyHashNotFoundException
from ..parsers import card_group, synergy_group
from ...models import (
    DBSession,
    Synergy,
    )


def load_existing_synergy(hash_id):
    synergy = DBSession.query(Synergy).filter_by(hash=hash_id).first()
    if synergy is None:
        raise SynergyHashNotFoundException(hash_id)

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

    name = synergy.name
    description = synergy.description

    card_list = card_group.to_list(synergy_cards)
    text_list = synergy_group.to_list(synergy_texts)
    lists = card_list + text_list
    lists.sort()
    form_cards_text = "\n".join([L[1] for L in lists])
    form_dict = {
        'form_cards_text': form_cards_text,
        'form_name': name,
        'form_description': description
    }
    return synergy.view_count, urls, counts, name, description, form_dict
