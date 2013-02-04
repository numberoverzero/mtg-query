##mtgquery.lib.pricing

from datetime import datetime
from ...lib.util import merge_dicts


def get_prices(cards, price_source, use_cached, max_cache_age=None, notifications=None):
    '''
    cards:: iterable of model.Card
    price_source:: model.PriceSource

    if use_cached, max_cache_age must be specified.
    max_cache_age is the age in seconds.

    returns a dictionary of {model.Card : price} where price is a float
    '''

    if use_cached:
        cached_prices = price_source.get_cached_card_prices(cards, notifications=notifications)
    else:
        cached_prices = dict()

    now = datetime.now()
    f_not_cached = lambda card: card not in cached_prices
    f_expired = lambda card: (now - cached_prices[card].cache_date).total_seconds() >= max_cache_age
    f_bad_cache = lambda card: f_not_cached(card) or f_expired(card)

    noncached_prices = price_source.get_live_card_prices(filter(f_bad_cache, cards), notifications=notifications)
    cached_prices = {card: cp.price for card, cp in cached_prices.iteritems()}

    return merge_dicts(cached_prices, noncached_prices)


def format_prices(trade_cards, prices):
    '''
    trade_cards:: iterable of model.TradeCard
    prices:: dict of {model.TradeCard: dict{quantity/price_ea/price_sum : float} }
    '''
    data = dict()
    for tc in trade_cards:
        card = tc.card
        cd = {}
        cd['quantity'] = tc.quantity
        if prices[card] is None:
            continue
        cd['price_each'] = prices[card]
        cd['price_sum'] = cd['price_each'] * cd['quantity']
        data[tc] = cd
    return data

from tcgplayer import TcgPriceManager

__pricing_managers = {
                    'tcgplayer': TcgPriceManager,
                    }
__default_pricing_manager = 'tcgplayer'


def parse_manager(name):
    if name not in __pricing_managers:
        name = __default_pricing_manager
    return __pricing_managers[name](None)
