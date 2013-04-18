import os
from ..util import rel_path
_here = rel_path(__file__)


def abs_path(filename):
    '''Supports dotted paths - help.foo is [DATAROOT]/help/foo'''
    name = filename.replace('.', os.sep)
    return os.path.join(_here, name)


def load(filename):
    '''Returns the contents of the given file in the data folder.'''
    filepath = abs_path(filename)
    with open(filepath) as f:
        data = f.read()
    try:
        data = unicode(data, encoding='utf-8')
    except UnicodeEncodeError:
        # Already unicode
        pass
    data = data.replace(u'\r\n', u'\n')
    return data


def load_lines(filename, skip_blank=False):
    lines = load(filename).split(u'\n')
    if skip_blank:
        lines = filter(bool, lines)
    return lines
