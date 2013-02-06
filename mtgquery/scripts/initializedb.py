import os
import sys
import transaction

import gen_help_links
from sqlalchemy import engine_from_config
from mtgquery.lib.alchemy_extensions import get_or_create

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from mtgquery.models import (
    DBSession,
    Base,
    PriceSource,
    TradeSlot
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def loadDBSession(argv):
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    sqlalchemy_url = os.environ.get('DATABASE_URL')
    settings['sqlalchemy.url'] = sqlalchemy_url

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    loadDBSession(argv)
    session = DBSession()
    __init_price_sources(session)
    __init_trade_slots(session)
    transaction.commit()
    gen_help_links.main()

price_sources = [
    'tcgplayer'
]


def __init_price_sources(session):
    for source_name in price_sources:
        price_source = get_or_create(session, PriceSource, name=source_name)
        session.merge(price_source)

trade_slots = [
    'stack1',
    'stack2'
]


def __init_trade_slots(session):
    for trade_slot_name in trade_slots:
        trade_slot = get_or_create(session, TradeSlot, name=trade_slot_name)
        session.merge(trade_slot)
