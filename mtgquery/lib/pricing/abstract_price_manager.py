from collections import defaultdict


class AbstractPriceManager(object):
    """Expected interface for a Price Manager"""

    def __init__(self, max_batch=None):
        """
        max_batch:
            number of price requests to queue before executing a batch query.
            If max_batch is 0 or None, all queries are executed immediately.
            If max_batch is negative, batched queries are only executed when forced.

            NOTE: single queries always return, regardless of batching rules
        """
        self._max_batch = max_batch
        self._queue = defaultdict(list)

    @property
    def queued_cards(self):
        for card in self._queue:
            yield card

    def get_single_price(self, card, notifications=None):
        """
        Retrieves the prices for a card.
        Any pending lookups for the same card are cleared
        """

        prices = self._lookup(card, notifications=notifications)
        if card in self.queued_cards:
            for callback in self._queue[card]:
                callback(card, prices)
            del self._queue[card]

        return prices

    def get_group_prices(self, cards, notifications=None):
        """
        Performs a batched lookup of cards.
        Also processes any queued cards.
        """
        prices = {}

        def append(card, card_prices):
            prices[card] = card_prices
        queue = lambda card: self.queue_lookup(card, append, suppress_processing=True)
        map(queue, cards)
        self.process_queue(notifications=notifications)
        return prices

    def queue_lookup(self, card, callback, suppress_processing=False):
        """
        When the queue is emptied, invokes callback(card, prices)

        suppress_processing will prevent the queue from emptying,
            even if other queue-clearing conditions are met.
        """
        self._queue[card].append(callback)
        if suppress_processing:
            return
        if (self.max_batch is None
            or self.max_batch == 0
            or len(self._queue) > self.max_batch):
            self.process_queue()

    def process_queue(self, notifications=None):
        """Completes all pending queries"""
        prices = self._batch_lookup(self._queue.keys(), notifications=notifications)
        for card in self._queue:
            callback_group = self._queue[card]
            for callback in callback_group:
                callback(card, prices[card])
        self._queue.clear()

    def _lookup(self, card, ignore_set=False, notifications=None):
        raise NotImplementedError("Using abstract price manager")

    def _batch_lookup(self, cards, notifications=None):
        raise NotImplementedError("Using abstract price manager")
