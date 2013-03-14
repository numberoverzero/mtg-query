import os
import sys

import gen_help_links
from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from mtgquery.models import (
    DBSession,
    Base,
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
    gen_help_links.main()
