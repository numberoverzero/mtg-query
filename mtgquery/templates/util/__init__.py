# util.__init__
import markupsafe
from mtgquery.lib.markdown_extensions import markdown_with_icons
from mtgquery.lib.beautifulsoup_utilities import add_class


def br(text):
    return text.replace('\n', markupsafe.Markup('<br />'))


def custom_markdown(text):
    return markdown_with_icons(text)


def mtg_description_escape(text):
    text = custom_markdown(text)
    text = add_class(text, 'table', 'table', 'table-bordered')
    return text
