## mtgquery.lib.parsers

from sets import resolve_set
from card_name import get_exact as get_exact_name
from card_group import cardcount_generator, card_regex
from synergy_group import synergytext_generator, synergy_text_regex

def to_string(cards):
    """
    returns a string containing all of the lines returned from to_list,
    in a format parsable with parse_string.
    """
    return "\n".join(t[1] for t in cards)