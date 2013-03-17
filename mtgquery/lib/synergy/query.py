from ...models import (
    DBSession,
    Synergy
)
from ..alchemy_extensions import get_last_n


def random_hash():
    return Synergy.get_random_hash()


def newest_synergies(n=10):
    data = []
    synergies = get_last_n(DBSession, Synergy, n, 'id', ['cards', 'texts'])
    for synergy in synergies:
        name = synergy.name if len(synergy.name) > 0 else "(Untitled)"
        data.append({
            'name': name,
            'length': len(synergy.cards) + len(synergy.texts),
            'url': '/s/{}'.format(synergy.hash)
        })
    return data
