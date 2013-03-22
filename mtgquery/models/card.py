from ..models import (
    Base,
    DBSession,
    InvalidDataException
)
from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey
)

from sqlalchemy.orm import relationship
from mtgquery.lib.parsers.sets import resolve_set
from mtgquery.lib.parsers.card_name import get_exact_name


class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    multiverse_id = Column(Integer, nullable=False)
    number = Column(Integer)
    power = Column(Text)
    toughness = Column(Text)

    artist_id = Column(Integer, ForeignKey('cardartists.id'))
    cost_id = Column(Integer, ForeignKey('cardcosts.id'))
    flavor_text_id = Column(Integer, ForeignKey('cardflavortexts.id'))
    name_id = Column(Integer, ForeignKey('cardnames.id'))
    oracle_rules_id = Column(Integer, ForeignKey('cardoraclerules.id'))
    printed_name_id = Column(Integer, ForeignKey('cardprintednames.id'))
    printed_rules_id = Column(Integer, ForeignKey('cardprintedrules.id'))
    printed_type_id = Column(Integer, ForeignKey('cardprintedtypes.id'))
    rarity_id = Column(Integer, ForeignKey('cardrarities.id'))
    set_id = Column(Integer, ForeignKey('cardsets.id'))
    type_id = Column(Integer, ForeignKey('cardtypes.id'))
    watermark_id = Column(Integer, ForeignKey('cardwatermarks.id'))

    @classmethod
    def interpolate_name_and_set(cls, name, set):
        '''
        name and set are both strings.  set can be None.

        if the specified set can't be found, will fall back to the most recent printing of the named card
        '''
        if name is None:
            raise InvalidDataException()
        special_name = get_exact_name(name)
        if special_name is not None:
            name = special_name

        card_name = DBSession.query(CardName).filter(CardName.name.ilike(name)).first()
        if card_name is None:
            raise InvalidDataException()

        possible_sets = [c.set.set for c in card_name.cards]
        best_set = resolve_set(set, possible_sets, card_name.name)

        card_set = DBSession.query(CardSet).filter(CardSet.set.ilike(best_set)).first()
        card = DBSession.query(Card).filter_by(name=card_name, set=card_set).first()
        return card


class CardArtist(Base):
    __tablename__ = 'cardartists'
    id = Column(Integer, primary_key=True)
    artist = Column(Text, nullable=False)
    cards = relationship("Card", backref='artist')


class CardCost(Base):
    __tablename__ = 'cardcosts'
    id = Column(Integer, primary_key=True)
    cost = Column(Text, nullable=False)
    cards = relationship("Card", backref='cost')


class CardFlavorText(Base):
    __tablename__ = 'cardflavortexts'
    id = Column(Integer, primary_key=True)
    flavor_text = Column(Text, nullable=False)
    cards = relationship("Card", backref='flavor_text')


class CardName(Base):
    __tablename__ = 'cardnames'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    cards = relationship("Card", backref='name')


class CardOracleRules(Base):
    __tablename__ = 'cardoraclerules'
    id = Column(Integer, primary_key=True)
    oracle_rules = Column(Text, nullable=False)
    cards = relationship("Card", backref='oracle_rules')


class CardPrintedName(Base):
    __tablename__ = 'cardprintednames'
    id = Column(Integer, primary_key=True)
    printed_name = Column(Text, nullable=False)
    cards = relationship("Card", backref='printed_name')


class CardPrintedRules(Base):
    __tablename__ = 'cardprintedrules'
    id = Column(Integer, primary_key=True)
    printed_rules = Column(Text, nullable=False)
    cards = relationship("Card", backref='printed_rules')


class CardPrintedType(Base):
    __tablename__ = 'cardprintedtypes'
    id = Column(Integer, primary_key=True)
    printed_type = Column(Text, nullable=False)
    cards = relationship("Card", backref='printed_type')


class CardRarity(Base):
    __tablename__ = 'cardrarities'
    id = Column(Integer, primary_key=True)
    rarity = Column(Text, nullable=False)
    cards = relationship("Card", backref='rarity')


class CardSet(Base):
    __tablename__ = 'cardsets'
    id = Column(Integer, primary_key=True)
    set = Column(Text, nullable=False)
    cards = relationship("Card", backref='set')


class CardType(Base):
    __tablename__ = 'cardtypes'
    id = Column(Integer, primary_key=True)
    type = Column(Text, nullable=False)
    cards = relationship("Card", backref='type')


class CardWatermark(Base):
    __tablename__ = 'cardwatermarks'
    id = Column(Integer, primary_key=True)
    watermark = Column(Text, nullable=False)
    cards = relationship("Card", backref='watermark')
