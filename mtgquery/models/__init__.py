##mtgquery.models

from ..lib.alchemy_extensions import get_or_create
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import ZopeTransactionExtension
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from card_models import (
    Card,
    CardArtist,
    CardCost,
    CardFlavorText,
    CardName,
    CardOracleRules,
    CardPrintedName,
    CardPrintedRules,
    CardPrintedType,
    CardRarity,
    CardSet,
    CardType,
    CardWatermark
)

from synergy_models import (
    Synergy,
    SynergyCard,
    SynergyText
)
