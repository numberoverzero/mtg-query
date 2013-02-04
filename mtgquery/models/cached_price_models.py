from ..models import (
    Base,
    DBSession,
    get_or_create
    )
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    Float,
    ForeignKey
    )

from sqlalchemy.orm import relationship, backref
from datetime import datetime

from ..lib.pricing import parse_manager


class CachedPrice(Base):
    __tablename__ = 'cachedprices'
    id = Column(Integer, primary_key=True)
    cache_date = Column(DateTime, nullable=False)
    card_id = Column(Integer, ForeignKey('cards.id'))
    price = Column(Float, nullable=False)
    price_source_id = Column(Integer, ForeignKey('pricesources.id'))


class PriceSource(Base):
    DEFAULT_SOURCE = 'tcgplayer'
    __tablename__ = 'pricesources'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    prices = relationship("CachedPrice", backref="price_source")
    trades = relationship("Trade", backref="price_source")

    def get_cached_card_prices(self, cards, notifications=None):
        cached_prices = filter(lambda cached_price: cached_price.card in cards, self.prices)
        return {cp.card: cp for cp in cached_prices}

    def get_live_card_prices(self, cards, notifications=None):
        prices = parse_manager(self.name).get_group_prices(cards, notifications=notifications)

        now = datetime.now()
        for card in prices:
            cached_price = get_or_create(DBSession, CachedPrice, card=card)
            cached_price.price = prices[card]
            cached_price.cache_date = now
            cached_price.price_source = self
            DBSession.add(cached_price)

        return prices
