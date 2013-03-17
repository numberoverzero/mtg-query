from ..util import simple_timer
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
    print '='*30
    print '='*30
    print "SHOULD BE DONE LOADING FROM DB"
    print '='*30
    print '='*30

    t = simple_timer()
    for synergy in synergies:
        name = synergy.name if len(synergy.name) > 0 else "(Untitled)"
        data.append({
            'name': name,
            'length': len(synergy.cards) + len(synergy.texts),
            'url': '/s/{}'.format(synergy.hash)
        })
    print "Loading synergy data took {} seconds".format(t())
    return data
