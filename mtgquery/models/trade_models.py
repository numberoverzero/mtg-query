from ..models import (
    Base,
    Card,
    DBSession,
    PriceSource
    )

from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Text,
    DateTime,
    Float,
    ForeignKey
    )

from sqlalchemy.orm import relationship, backref

from ..lib import base58
from ..lib.alchemy_extensions import has_model
from ..lib.util import DEBUG
import random

class Trade(Base):
    '''
    represents a trade submit.
    includes metadata about the trade submission (cache, pricer)
    '''
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, nullable=False)
    is_public = Column(Boolean)
    price_source_id = Column(Integer, ForeignKey('pricesources.id'))
    trade_cards = relationship("TradeCard", backref="trade")
    use_cached = Column(Boolean)
    view_count = Column(Integer)
    hash = Column(Text, unique=True)
    hash_rand_len = Column(Integer)
    hash_seq_len = Column(Integer)
    name = Column(Text)

    def generate_hash(self, seq_len=6, rand_len=6):
        '''
        Generates a hash from the sequential id.
        '''

        #Guarantee we have a sequential id
        session = DBSession()
        session.add(self)
        session.flush()
        
        #Generate the hash from sequential
        self.hash = base58.from_seq_with_rand(
            self.id, random, seq_len, rand_len)

        #Save hash info
        self.hash_rand_len = rand_len
        self.hash_seq_len = seq_len

        session = DBSession()
        session.add(self)
        session.flush()

        return self.hash

    def random_generate_unique(self, length=5):
        '''
        Randomly generates a hash of the given length.
        Will continue brute-forcing until it finds one.
        Will run forever if there are no available hashes.
        '''
        attempted = [0]
        def validate((seq, hash)):
            attempted[0] += 1
            if has_model(DBSession, Trade, hash = hash):
                return -1
            DEBUG("Generated Trade Hash <{}> in {} tries.".format(hash, attempted[0]))
            return 1

        seq, self.hash = base58.gen_random(exact_length = length, validate = validate)
        
        #Save new hash
        session = DBSession()
        session.add(self)
        session.flush()


class TradeCard(Base):
    '''a card listed in a trade, and metadata (such as slot)'''
    __tablename__ = 'tradecards'
    id = Column(Integer, primary_key=True)
    card = relationship("Card")
    card_id = Column(Integer, ForeignKey('cards.id'))
    index = Column(Integer)
    quantity = Column(Integer)
    slot_id = Column(Integer, ForeignKey('tradeslots.id'))
    trade_id = Column(Integer, ForeignKey('trades.id'))

class TradeSlot(Base):
    __tablename__ = 'tradeslots'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    trade_cards = relationship("TradeCard", backref="slot")