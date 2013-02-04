# -*- coding: utf-8 -*-
from unicode_card_names import special_cards
special_cards_exact = []
for card_name in special_cards.split('\n'):
    if len(card_name) == 0:
        continue
    card_name = unicode(card_name, encoding='utf-8').strip()
    special_cards_exact.append(card_name)

valid_spellings = {}
valid_replacements = [u'ae', u'æ']
for exact in special_cards_exact:
    for replacement in valid_replacements:
        valid = exact.replace(u'Æ', replacement)
        valid_spellings[valid] = exact


def ci_contains(string):
    ci_string = string.lower()
    for spelling in valid_spellings:
        if ci_string == spelling.lower():
            return spelling
    return None


def get_exact(string):
    try_resolve = ci_contains(string)
    if try_resolve is None:
        return None
    return valid_spellings[try_resolve]
