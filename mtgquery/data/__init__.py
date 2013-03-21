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
    return data
