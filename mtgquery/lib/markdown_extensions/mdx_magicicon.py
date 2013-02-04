import markdown
from markdown.inlinepatterns import Pattern
from mtgquery.lib.gatherer_icons import get_icon_url

ICON_RE = r'(\{)(.*?)\}'


class AttrTagPattern(Pattern):
    """
    Return element of type `tag` with a text attribute of group(3)
    of a Pattern and with the html attributes defined with the constructor.

    """
    def __init__(self, pattern, tag, attrs):
        Pattern.__init__(self, pattern)
        self.tag = tag
        self.attrs = attrs

    def handleMatch(self, m):
        icon_raw = m.group(3)
        url = get_icon_url(icon_raw)
        if url is None:
            return '{' + icon_raw + '}'

        el = markdown.util.etree.Element(self.tag)
        el.set('src', url)
        for (key, val) in self.attrs.items():
            el.set(key, val)
        return el


class MagicIconExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        icon_tag = AttrTagPattern(ICON_RE, 'img', {'class': 'magicicon'})
        md.inlinePatterns.add('magicicon', icon_tag, '_end')


def makeExtension(configs=None):
    return MagicIconExtension(configs=configs)
