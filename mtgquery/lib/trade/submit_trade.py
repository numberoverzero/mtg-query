from datetime import datetime
from ...lib.parsers import cardcount_generator
from ..util.rate_limiting_generator import line_generator, rate_limit
from ..notifications import GenericNotification
from ...models import (
    DBSession,
    Card,
    Trade,
    TradeCard,
    TradeSlot,
    PriceSource
    )


def submit_new_trade(card_stacks, name, source, use_cached):
    '''returns the hash that the submitted trade can be found at'''

    notifications = []

    #Cut down our stacks to max lines
    tmp_stacks = []
    stack_names = "One", "Two"
    for index in [0, 1]:
        card_gen = line_generator(card_stacks[index], False)
        card_limit = 40
        card_valid = lambda line: len(line.strip()) > 0
        exceeded_fmt = "Stack {} truncated: maximum of {} cards"
        card_on_limit = lambda (i, limit, value): notifications.append(GenericNotification(exceeded_fmt.format(stack_names[index], card_limit)))
        card_rate_gen = rate_limit(card_gen, card_limit, card_valid, card_on_limit)
        tmp_stacks.append('\n'.join(card_rate_gen))
    card_stacks = tmp_stacks

    price_source = DBSession.query(PriceSource).filter_by(name=source).first()
    if price_source is None:
        # Try again with default source
        original_source = source
        source = PriceSource.DEFAULT_SOURCE
        price_source = DBSession.query(PriceSource).filter_by(name=source).first()
        if price_source is None:  # Default price source isn't found, we've got problems
            raise TypeError("Invalid price source <{0}>".format(original_source))
        notifications.append(GenericNotification("Couldn't find price source {}, using default {}".format(original_source, source)))

    use_cached = use_cached == "on"

    trade = Trade(create_date=datetime.now(), price_source=price_source,
        use_cached=use_cached, view_count=0, is_public=True, name=name)
    # For now we're using random generation, since the number of collisions over the 600mil+ possible values is... low.
    #trade.generate_hash()
    trade.random_generate_unique()
    DBSession.add(trade)

    index = 0  # We're not using the automatic index because it still increments on valid regex but non-existant card names

    trade_slot_names = ['stack1', 'stack2']
    for card_stack, trade_slot_name in zip(card_stacks, trade_slot_names):
        for card_name, count, set, _ in cardcount_generator(card_stack, notifications=notifications):
            card = Card.interpolate_name_and_set(card_name, set, notifications=notifications)
            if card is None:
                continue
            index += 1
            trade_slot = DBSession.query(TradeSlot).filter_by(name=trade_slot_name).first()

            trade_card = TradeCard(trade=trade, card=card, index=index, quantity=count, slot=trade_slot)
            DBSession.add(trade_card)
        index = 0

    return trade.hash, notifications
