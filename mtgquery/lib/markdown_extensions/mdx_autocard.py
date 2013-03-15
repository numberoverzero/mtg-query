import markdown
from markdown.inlinepatterns import Pattern
from ...models.card_models import Card

# CARD_RE = re.compile(r'''
#     (\[\[)           # Open square brackets
#     (.+?)            # Card name
#     (:([^"]+?))?     # Optional set specifier (we don't want to grab quotes in case they're specifying text)
#     (\s*"(.+?)")?    # Optional text for the link
#     (\]\])           # Close square brackets
# ''', re.VERBOSE)

CARD_RE = r'(\[\[)([^:^"]+?)(:([^"]+?))?("(.+?)")?(\]\])'
BASE_CARD_URL = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={}&type=card'
TEMPLATE = u'<img class="card-corners" src = "{}" alt="{}" /></img>'


class AutoCardPattern(Pattern):
    def handleMatch(self, m):
        name = m.group(3)
        if name:
            name = name.strip()
        set = m.group(5)
        if set:
            set = set.strip()
        link_text = m.group(7)

        card = Card.interpolate_name_and_set(name, set)

        if card is None:  # Not a valid card, return the raw input
            return u''.join(m.groups('')[1:])

        src = BASE_CARD_URL.format(card.multiverse_id)
        alt = u"{} ({})".format(card.name.name, card.set.set)
        content = TEMPLATE.format(src, alt)

        el = markdown.util.etree.Element('a')
        el.set('class', 'card-tooltip')
        el.set('rel', 'tooltip')
        el.set('data-title', content)
        if not link_text:
            link_text = card.name.name
        el.text = link_text
        return el


class AutoCardExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        auto_card = AutoCardPattern(CARD_RE)
        md.inlinePatterns.add('autocard', auto_card, '_end')


def makeExtension(configs=None):
    return AutoCardExtension(configs=configs)
