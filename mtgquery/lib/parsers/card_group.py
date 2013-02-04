from mtgquery.lib.notifications import InvalidLine
import re
card_regex = re.compile(r"^((?P<count>\d+)\s)?(?P<card>[^:]+)\s*(:\s*(?P<set>.*))?$")


def skip_line(line, re_ignores):
    if re_ignores is None:
        return False
    for regex in re_ignores:
        if regex.search(line):
            #Found a matching line, skip this line
            return True
    return False


def cardcount_generator(string, notifications=None, re_ignores=None):
    lines = string.split("\n")
    for index, line in enumerate(lines):
        line = line.strip()
        #Check if we should ignore this line
        if skip_line(line, re_ignores):
            continue

        match = card_regex.search(line)
        if not match:
            if len(line) == 0:
                continue
            if notifications is not None:
                notifications.append(InvalidLine(line))
            continue

        count = match.group('count')
        if count:
            count = count.strip()
        count = int(count) if count else 1

        card = match.group('card')
        if card:
            card = card.strip()

        set = match.group('set')
        if set:
            set = set.strip()

        yield card, count, set, index


def to_list(cards):
    """
    returns a list of (index, string) tuples which can be merged with other lists (like synergies)
    """
    L = []
    fmt = u"{} {} : {}"
    for c in cards:
        s = fmt.format(c.quantity, c.card.name.name, c.card.set.set)
        L.append((c.index, s))
    L.sort()
    return L
