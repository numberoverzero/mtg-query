# -*- coding: utf-8 -*-
from ...data import load
special_cards_exact = []
for card_name in load('cards.special_names').split('\n'):
    if len(card_name) == 0:
        continue
    card_name = unicode(card_name, encoding='utf-8').strip()
    special_cards_exact.append(card_name)

valid_spellings = {}
ci_valid_spellings = {}
replacements = [
    (u'æ', u'ae'),
    (u'Æ', u'ae'),
    (u'é', u'e'),
]

for exact in special_cards_exact:
    for replacement in replacements:
        valid = exact.replace(*replacement)
        if valid == exact:  # No replacement
            continue
        valid_spellings[valid] = exact
        ci_valid_spellings[valid.lower()] = exact


def ci_contains(string):
    ci_string = string.lower()
    for spelling in valid_spellings:
        if ci_string == spelling.lower():
            return spelling
    return None


def get_exact_name(string):
    try_resolve = ci_contains(string)
    if try_resolve is None:
        return None
    return valid_spellings[try_resolve]
