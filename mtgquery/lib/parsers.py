# -*- coding: utf-8 -*-
from mtgquery.models import DBSession, InvalidDataException
from mtgquery.models.card import Card, CardName, CardSet
from mtgquery import data

card_name_replacements = {}


def load_replacements():
    global card_name_replacements

    # Load unicode card names, such as Æther Flash
    unicode_replacements = [(u'Æ', u'ae'), (u'æ', u'ae'), (u'é', u'e')]
    unicode_names = data.load_lines('cards.special_names', skip_blank=True)
    for exact in unicode_names:
        for replacement in unicode_replacements:
            valid = exact.replace(*replacement)
            if valid != exact:
                card_name_replacements[valid.lower().strip()] = exact

sets = data.load_lines('cards.sets', skip_blank=True)
ci_descending_set_names = [set.lower() for set in reversed(sets)]


def card_from(name, set):
        '''
        name and set are both strings.  set can be None.

        if the specified set can't be found, will fall back to the most recent printing of the named card
        '''
        if not name:
            raise InvalidDataException(u"Card name cannot be blank")
        name = card_name_replacements.get(name.lower(), name)

        card_name = DBSession.query(CardName).filter(CardName.name.ilike(name)).first()
        if card_name is None:
            raise InvalidDataException(u"Unknown card {}".format(name))

        possible_sets = [c.set.set for c in card_name.cards]
        best_set = resolve_set(set, possible_sets, card_name.name)
        if best_set is None:
            raise InvalidDataException(u"Unknown set {}".format(set))

        card_set = DBSession.query(CardSet).filter(CardSet.set.ilike(best_set)).first()
        card = DBSession.query(Card).filter_by(name=card_name, set=card_set).first()
        return card


def __set_cmp__(set_name_1, set_name_2):
    '''
    set1 < set2 :: -1
    set1 == set2 :: 0
    set1 > set2 :: +1

    DO NOT pass aliases into this function - interpolate to valid set names first.
    sorts in DESCENDING ORDER (newest set first)
    '''
    set_name_1 = set_name_1.lower()
    set_name_2 = set_name_2.lower()

    in1 = set_name_1 in ci_descending_set_names
    in2 = set_name_2 in ci_descending_set_names

    if in1 and in2:
        return cmp(ci_descending_set_names.index(set_name_1),
                   ci_descending_set_names.index(set_name_2))
    elif in1 and not in2:
        return 1
    elif in2 and not in1:
        return -1
    else:
        return 0


def resolve_set(set, sets, card_name):
    '''
    for a given set name (possible None), return the best set out of the possible sets.
    if the given set isn't one of the values in sets, returns the most recent set in sets.
    '''

    if not sets:
        return None

    #Exact case-sensitive name
    if set in sets:
        return set

    sorted_sets = sorted(sets, cmp=__set_cmp__)

    #Default to first set for None
    if set is None:
        return sorted_sets[0]

    ci_sorted_sets = [s.lower() for s in sorted_sets]
    ci_set = set.lower()

    #Exact case-insensitive name
    for index, ci_ss in enumerate(ci_sorted_sets):
        if ci_set == ci_ss:
            return sorted_sets[index]

    #Partial case-insensitive name
    for index, ci_ss in enumerate(ci_sorted_sets):
        if ci_set in ci_ss:
            return sorted_sets[index]

    #No matches
    return sorted_sets[0]
