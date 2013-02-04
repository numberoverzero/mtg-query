##mtgquery.lib.markdown_extensions

import markdown
from mdx_magicicon import MagicIconExtension
from mdx_autocard import AutoCardExtension

extensions = ['tables', 'fenced_code', 'sane_lists', MagicIconExtension(), AutoCardExtension()]

internal_extensions = list(extensions)
internal_extensions.extend(['attr_list'])

icon_markdown = markdown.Markdown(safe_mode='escape', extensions=extensions)
internal_icon_markdown = markdown.Markdown(safe_mode='escape', extensions=internal_extensions)

del icon_markdown.inlinePatterns['image_link']
del icon_markdown.inlinePatterns['image_reference']


def internal_markdown_with_icons(string):
    return internal_icon_markdown.convert(string)


def markdown_with_icons(string):
    return icon_markdown.convert(string)
