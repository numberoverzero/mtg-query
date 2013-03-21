from ..lib.beautifulsoup_utilities import add_class
from ..lib.markdown_extensions import internal_markdown_with_icons
from ..data import load

_cache = {}
_files = {
    'site': "help.basic_text",
    'markdown': "help.markdown_text",
    'symbols': "help.magic_symbols"
}


def render_file(filename):
    '''filename must be a file in the local directory'''
    text = load(filename)
    text = internal_markdown_with_icons(text)
    text = add_class(text, 'table', 'table', 'table-bordered', 'table-short')
    return text


def load_html(section):
    if section not in _files:
        return ''
    if section not in _cache:
        filename = _files[section]
        _cache[section] = render_file(filename)
    return _cache[section]


def preheat_cache():
    for section in _files:
        print "preheating {}".format(section)
        load_html(section)
