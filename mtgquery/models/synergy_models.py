import transaction
from ..models import (
    Base,
    DBSession
)

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from ..lib import base58
from ..lib.alchemy_extensions import has_model, get_random
from ..lib.util import DEBUG
import random


class Synergy(Base):
    __tablename__ = 'synergies'
    id = Column(Integer, primary_key=True)
    cards = relationship("SynergyCard", backref="synergy")
    texts = relationship("SynergyText", backref="synergy")
    create_date = Column(DateTime, nullable=False)
    description = Column(Text)
    is_public = Column(Boolean)
    name = Column(Text)
    view_count = Column(Integer)
    hash = Column(Text, unique=True)
    hash_rand_len = Column(Integer)
    hash_seq_len = Column(Integer)

    def generate_hash(self, seq_len=6, rand_len=6):
        '''
        Generates a hash from the sequential id.
        '''

        #Guarantee we have a sequential id
        session = DBSession()
        session.add(self)
        transaction.commit()

        #Generate the hash from sequential
        self.hash = base58.from_seq_with_rand(
            self.id, random, seq_len, rand_len)

        #Save hash info
        self.hash_rand_len = rand_len
        self.hash_seq_len = seq_len

        session = DBSession()
        session.add(self)
        transaction.commit()

        return self.hash

    @classmethod
    def get_random_hash(cls):
        '''
        Get a random synergy hash
        '''
        synergy = get_random(DBSession, Synergy, 'id')
        if synergy is None:
            return None
        return synergy.hash

    def random_generate_unique(self, length=5):
        '''
        Randomly generates a hash of the given length.
        Will continue brute-forcing until it finds one.
        Will run forever if there are no available hashes.
        '''
        attempted = [0]

        def validate((seq, hash)):
            attempted[0] += 1
            if has_model(DBSession, Synergy, hash=hash):
                return -1
            DEBUG("Generated Synergy Hash <{}> in {} tries.".format(hash, attempted[0]))
            return 1

        seq, self.hash = base58.gen_random(exact_length=length, validate=validate)

        #Save new hash
        session = DBSession()
        session.add(self)
        transaction.commit()


class SynergyCard(Base):
    '''a card listed in a synergy, and metadata (such as ordering, quantity)'''
    __tablename__ = 'synergycards'
    id = Column(Integer, primary_key=True)
    card = relationship("Card")
    card_id = Column(Integer, ForeignKey('cards.id'))
    index = Column(Integer)
    quantity = Column(Integer)
    synergy_id = Column(Integer, ForeignKey('synergies.id'))
    specified_set = Column(Boolean)


class SynergyText(Base):
    '''
    a short piece of text to overlay a blank card with.
    this is useful for indicating that a class of cards can be used
    Examples:   "Creature with infect"
                "Mana"
                "Artifact with cmc 0 or 1"
    '''
    __tablename__ = 'synergytexts'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    quantity = Column(Integer)
    synergy_id = Column(Integer, ForeignKey('synergies.id'))
    text = Column(Text)
