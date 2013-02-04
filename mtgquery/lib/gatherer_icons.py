
sizes = [
    'small',
    'medium',
    'large'
]

icons = [
    'tap',
    'untap',

    #Single, double split, phyrexian
    'b', '2b', 'bp',
    'g', '2g', 'gp',
    'r', '2r', 'rp',
    'u', '2u', 'up',
    'w', '2w', 'wp',

    #Colorless,
    'x',
    '1000000'
]

#Colorless 0-16
icons.extend(str(i) for i in xrange(17))

#Split
split = [
    'bg', 'br',
    'gu', 'gw',
    'rg', 'rw',
    'ub', 'ur',
    'wb', 'wu',
]
icons.extend(split)

split_reverse = {s[::-1]: s for s in split}

#Images known not to exist
skip = [
    ('large', 'bp'),
    ('large', 'gp'),
    ('large', 'rp'),
    ('large', 'up'),
    ('large', 'wp')
]

shorthand = {
    't': 'tap',
    'ut': 'untap'
}

size_lookup = {
    's': 'small',
    'small': 'small',
    'm': 'medium',
    'medium': 'medium',
    'l': 'large',
    'large': 'large'
}
default_size = 'small'


def has_icon(size, name):
    '''Checks shorthand representations and split reversal'''
    if name in shorthand:
        name = shorthand[name]
    icon = (size, name)
    return (
        icon not in skip
        and (name in icons or name in split_reverse)
    )


def get_icon(icon_raw):
    '''Performs any necessary transformations on size and name to coerce to valid entries'''
    pieces = icon_raw.split(':', 2)
    if len(pieces) == 1:
        name = icon_raw
        size = default_size
    else:
        name = pieces[0]
        size = pieces[1].lower()
        # For now, we're not going to fall back to small,
        # since they may have meant to use the literal text tap:blargh instead of getting {tap:small}
        #size = size_lookup.get(size, default_size)
        size = size_lookup.get(size, None)
        if size is None:
            return None
    name = name.lower()

    if not has_icon(size, name):
        return None
    if name in shorthand:
        name = shorthand[name]
    if name in split_reverse:
        name = split_reverse[name]
    return (size, name)

url = """http://gatherer.wizards.com/Handlers/Image.ashx?size={}&name={}&type=symbol"""


def get_icon_url(icon_raw):
    icon = get_icon(icon_raw)
    if icon is None:
        return None
    size, name = icon
    return url.format(size, name)


def parse_icon_url(icon_raw):
    '''figures out size'''
    pieces = icon_raw.split(':', 2)
    if len(pieces) == 1:
        name = icon_raw
        size = default_size
    else:
        name = pieces[0]
        size = pieces[1].lower()
        size = size_lookup.get(size, default_size)

    return get_icon_url(size, name)
