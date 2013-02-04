import re
synergy_text_regex = re.compile(r"^((?P<count>\d+)\s)?(#(?P<text>.+?))$")


def synergytext_generator(string, notifications=None):
    lines = string.split("\n")
    for index, line in enumerate(lines):
        line = line.strip()
        match = synergy_text_regex.search(line)
        if not match:
            continue

        count = match.group('count')
        if count:
            count = count.strip()
        count = int(count) if count else 1

        text = match.group('text')
        if text:
            text = text.strip()

        yield text, count, index


def to_list(texts):
    """
    returns a list of (index, string) tuples which can be merged with other lists (like cards)
    """
    L = []
    fmt = "{} #{}"
    for t in texts:
        s = fmt.format(t.quantity, t.text)
        L.append((t.index, s))
    L.sort()
    return L
