##mtgquery.lib.help.__init__
import os
from ..beautifulsoup_utilities import add_class
from ..markdown_extensions import internal_markdown_with_icons
from ..util import rel_path
from ..util.unicode_util import AutomagicUnicode

REL = rel_path(__file__)
namefmt = REL + os.sep + "{}"

# These are replacements that need to be used
# before running markdown, because markdown can't handle them well.
# For example - markdown's table processor has no way of escaping its column dividers.
replacements = [
    (r'\|', '&pipe;', '|')
]


def pre_markdown(text):
    for input, tmp, output in replacements:
        text = text.replace(input, tmp)
    return text


def post_markdown(text):
    for input, tmp, output in replacements:
        text = text.replace(tmp, output)
    return text


def markdown_file(filename):
    '''filename must be a file in the local directory'''
    with open(namefmt.format(filename)) as f:
        text = f.read()

    text = pre_markdown(text)

    magic = AutomagicUnicode(text)
    with magic:
        magic.str = internal_markdown_with_icons(magic.str)
        magic.str = add_class(magic.str, 'table', 'table', 'table-bordered', 'table-short')

    text = post_markdown(magic.str)

    return text

#basic_contents = markdown_file("basic_text")
text_contents = markdown_file("markdown_text")
magic_symbols = markdown_file("magic_symbols")

basic_contents = "TEST"
#text_contents = "TEST"
#magic_symbols = "TEST"
