import os
from abstract_price_manager import AbstractPriceManager
from ..notifications import GenericNotification
from ...lib import http
from ..util import rel_path

REL = rel_path(__file__)
URL_BASE = 'http://partner.tcgplayer.com/x2/phl.asmx/p?pk=AUTOANY&s={}&p={}'
set_file = REL + os.sep + 'tcg_sets'
UNKNOWN_SET_PRICE = "Could not find prices for {} in set {}.  Using prices from any set."

# Load up our real set name -> tcg set name mapping
__setmap = {}
with open(set_file) as f:
    lines = f.read()
    for line in lines.split('\n'):
        try:
            real, tcgset = line.split('=', 1)
            __setmap[real] = tcgset
        except:
            continue


def card_url(card, ignore_set=False):
        name = card.name.name
        set = '' if ignore_set else __setmap.get(card.set.set, '')
        return URL_BASE.format(
            http.uri_encode(set),
            http.uri_encode(name)
            )


class TcgPriceManager(AbstractPriceManager):

    def __init__(self, max_batch=None):
        AbstractPriceManager.__init__(self, max_batch)

    def price_from_html(self, html):
        xml = http.get_xml(html)
        product = xml.find('product')
        if product is None:
            return None
        return float(product.find('avgprice').text)

    def _lookup(self, card, ignore_set=False, notifications=None):
        '''If ignore_set is false and no results are found, sends a second request for ANY set.'''
        html = http.get_html(card_url(card, ignore_set))
        price = self.price_from_html(html)
        if price is None:
            if ignore_set:  # Couldn't find a price in any set
                return 0.0
            else:  # Try to find the price for the card in any set
                if notifications is not None:
                    notifications.append(
                        GenericNotification(UNKNOWN_SET_PRICE.format(card.name.name, card.set.set))
                        )
                return self._lookup(card, ignore_set=True)

    def _batch_lookup(self, cards, notifications=None):

        # Try to find set-specific prices first
        urls = [card_url(card, ignore_set=False) for card in cards]

        prices = {}
        not_found = []

        def process((html, card)):
            price = self.price_from_html(html)
            if price is None:
                not_found.append(card)
            else:
                prices[card] = price
        map(process, zip(http.get_htmls(urls), cards))

        # Found all our prices the first time, bail early
        if len(not_found) == 0:
            return prices

        # Retry lookups for cards we don't have prices for, but take results for any set
        urls = [card_url(card, ignore_set=True) for card in not_found]

        def reprocess((html, card)):
            if notifications is not None:
                notifications.append(
                    GenericNotification(UNKNOWN_SET_PRICE.format(card.name.name, card.set.set))
                    )
            price = self.price_from_html(html)
            if price is None:
                price = 0.0
            prices[card] = price
        map(reprocess, zip(http.get_htmls(urls), not_found))

        return prices
