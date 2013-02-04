from ..exceptions import TradeHashNotFoundException
from ..pricing import get_prices, format_prices
from ..parsers import to_string
from ..parsers.card_group import to_list
from ...models import (
    DBSession,
    Trade
    )


def load_existing_trade(hash_id, notifications=None):

    if notifications is None:
        notifications = []
    trade = DBSession.query(Trade).filter_by(hash=hash_id).first()
    if trade is None:
        raise TradeHashNotFoundException(hash_id)

    #Update view count
    trade.view_count += 1
    DBSession.add(trade)

    trade_cards = trade.trade_cards
    trade_cards.sort(key=lambda c: c.index)

    max_cache_age = 30 * 60  # Thirty minutes (should be fast enough for new sets coming out)

    cards = [tc.card for tc in trade_cards]
    card_prices = get_prices(cards, trade.price_source, trade.use_cached, max_cache_age, notifications=notifications)

    slots = ['stack1', 'stack2']
    stacks = [[], []]
    for trade_card in trade_cards:
        index = slots.index(trade_card.slot.name)
        stacks[index].append(trade_card)

    prices = format_prices(trade_cards, card_prices)

    #format dictionaries into row/columns for table
    headers = ['#', 'Card Name', 'Set', 'Price', 'Copies', 'Total']

    grand_totals = [0.0] * 2
    tables = [[], []]
    for index in [0, 1]:
        for tc in stacks[index]:
            tc_prices = prices.get(tc, None)
            if tc_prices is None:
                continue
            row = []
            row.append(tc.index)
            row.append(tc.card.name.name)
            row.append(tc.card.set.set)
            row.append(tc_prices['price_each'])
            row.append(tc_prices['quantity'])
            row.append(tc_prices['price_sum'])
            grand_totals[index] += tc_prices['price_sum']
            tables[index].append(row)

    diff = grand_totals[0] - grand_totals[1]
    name = trade.name

    form_dict = {
        'form_name': name,
        'form_stack_1_text': to_string(to_list(stacks[0])),
        'form_stack_2_text': to_string(to_list(stacks[1])),
        'form_source_value': trade.price_source.name,
        'form_use_cached': trade.use_cached,
    }

    return trade.view_count, name, headers, tables, grand_totals, diff, form_dict
