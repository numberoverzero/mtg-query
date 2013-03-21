from mtgquery.models import InvalidDataException


ascending_set_names = [
    "Limited Edition Alpha",
    "Limited Edition Beta",
    "Unlimited Edition",
    "Arabian Nights",
    "Antiquities",
    "Revised Edition",
    "Legends",
    "The Dark",
    "Fallen Empires",
    "Fourth Edition",
    "Ice Age",
    "Chronicles",
    "Homelands",
    "Alliances",
    "Mirage",
    "Visions",
    "Fifth Edition",
    "Portal",
    "Weatherlight",
    "Tempest",
    "Stronghold",
    "Exodus",
    "Portal Second Age",
    "Unglued",
    "Urza's Saga",
    "Urza's Legacy",
    "Classic Sixth Edition",
    "Urza's Destiny",
    "Portal Three Kingdoms",
    "Starter 1999",
    "Mercadian Masques",
    "Battle Royale Box Set",
    "Nemesis",
    "Starter 2000",
    "Prophecy",
    "Invasion",
    "Beatdown Box Set",
    "Planeshift",
    "Seventh Edition",
    "Apocalypse",
    "Odyssey",
    "Torment",
    "Judgement",
    "Onslaught",
    "Legions",
    "Scourge",
    "Eighth Edition",
    "Mirrodin",
    "Darksteel",
    "Fifth Dawn",
    "Champions of Kamigawa",
    "Unhinged",
    "Betrayers of Kamigawa",
    "Saviors of Kamigawa",
    "Ninth Edition",
    "Ravnica: City of Guilds",
    "Guildpact",
    "Dissension",
    "Coldsnap",
    "Time Spiral",
    "Time Spiral \"Timeshifted\"",
    "Planar Chaos",
    "Future Sight",
    "Tenth Edition",
    "Lorwyn",
    "Duel Decks: Elves vs. Goblins",
    "Morningtide",
    "Shadowmoor",
    "Eventide",
    "From the Vault: Dragons",
    "Shards of Alara",
    "Duel Decks: Jace vs. Chandra",
    "Conflux",
    "Duel Decks: Divine vs. Demonic",
    "Alara Reborn",
    "Magic 2010",
    "From the Vault: Exiled",
    "Planechase",
    "Zendikar",
    "Duel Decks: Garruk vs. Liliana",
    "Premium Deck Series: Slivers",
    "Worldwake",
    "Duel Decks: Phyrexia vs. the Coalition",
    "Rise of the Eldrazi",
    "Archenemy",
    "Magic 2011",
    "From the Vault: Relics",
    "Duel Decks: Elspeth vs. Tezzeret",
    "Scars of Mirrodin",
    "Premium Deck Series: Fire and Lightning",
    "Mirrodin Besieged",
    "Duel Decks: Knights vs. Dragons",
    "New Phyrexia",
    "Magic: The Gathering-Commander",
    "Magic 2012",
    "From the Vault: Legends",
    "Duel Decks: Ajani vs. Nicol Bolas",
    "Innistrad",
    "Premium Deck Series: Graveborn",
    "Dark Ascension",
    "Duel Decks: Venser vs. Koth",
    "Avacyn Restored",
    "Planechase 2012 Edition",
    "Magic 2013",
    "From the Vault: Realms",
    "Duel Decks: Izzet vs. Golgari",
    "Return to Ravnica",
    "Commander's Arsenal",
    "Gatecrash"
]

#upper case for case invariant searches
ci_ascending = [set.upper() for set in ascending_set_names]

descending_set_names = list(reversed(ascending_set_names))
ci_descending = [set.upper() for set in descending_set_names]

replacements = {
    'FTV': 'From The Vault',
    'DD': 'Duel Decks',
    'PDS': 'Premium Deck Series',
    'M10': 'Magic 2010',
    'M11': 'Magic 2011',
    'M12': 'Magic 2012',
    'M13': 'Magic 2013',
}


def is_partial_of_set_name(set):
    ci_set = set.upper()
    for set in ci_descending:
        if ci_set in set:
            return from_ci(set)
    return False


def from_ci(ci_set):
    index = ci_ascending.index(ci_set)
    return ascending_set_names[index]


def set_cmp(set_name_1, set_name_2):
    '''

    condition :: ret_val
    set1 < set2 :: negative
    set1 == set2 :: zero
    set1 > set2 :: positive

    DO NOT pass aliases into this function - interpolate to valid set names first.
    raises ValueError if either name isn't in descending_set_names.

    sorting a set with set_cmp yields a list of sets sorted in DESCENDING ORDER (newest set first)
    for example:
        some_sets = [
            "Duel Decks: Izzet vs. Golgari",
            "From the Vault: Realms",
            "Magic 2013",
            "Commander's Arsenal",
            "Return to Ravnica",
            ]
        print "\n".join(sorted(some_sets, cmp=set_cmp))
    '''
    set_name_1 = set_name_1.upper()
    set_name_2 = set_name_2.upper()

    # Sets not in the global list always compare as less than sets in the list
    in1 = set_name_1 in ci_descending
    in2 = set_name_2 in ci_descending

    if in1 and in2:
        # Both sets are in the list
        return cmp(ci_descending.index(set_name_1), ci_descending.index(set_name_2))
    elif in1 and not in2:
        return 1
    elif in2 and not in1:
        return -1
    else:
        # Neither set is in the list
        return 0


def resolve_set(set, sets, card_name):
    '''
    for a given set name (possible None), return the best set out of the possible sets.
    if the given set isn't one of the values in sets, returns the most recent set in sets.
    '''

    if sets is None or len(sets) == 0:
        raise InvalidDataException()

    #Exact case-sensitive name
    if set in sets:
        return set

    sorted_sets = sorted(sets, cmp=set_cmp)

    #Default to first set for None
    if set is None:
        return sorted_sets[0]

    ci_sorted_sets = [s.upper() for s in sorted_sets]
    ci_set = set.upper()

    #Exact case-insensitive name
    for index, ci_ss in enumerate(ci_sorted_sets):
        if ci_set == ci_ss:
            return sorted_sets[index]

    #Partial case-insensitive name
    for index, ci_ss in enumerate(ci_sorted_sets):
        if ci_set in ci_ss:
            return sorted_sets[index]

    #No matches

    #real_set = is_partial_of_set_name(set)
    #if real_set:
    #    #it's a real set, just not valid for this card
    #    raise InvalidDataException()
    #else:
    #    #this isn't a real set
    #    raise InvalidDataException()
    return sorted_sets[0]
