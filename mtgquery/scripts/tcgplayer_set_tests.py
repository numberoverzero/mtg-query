import xml.etree.ElementTree
import eventlet
from eventlet.green import urllib2
pool = eventlet.GreenPool()


def get_html(url):
    """Blocking call, use get_htmls for batch gets"""
    return urllib2.urlopen(url).read()


def get_htmls(urls):
    return pool.imap(get_html, urls)


def get_xml(html):
    """Converts html responses"""
    return xml.etree.ElementTree.fromstring(html)


def uri_encode(string):
    """Escapes everything"""
    return urllib2.quote(string, '')

URL_BASE = 'http://partner.tcgplayer.com/x2/phl.asmx/p?pk=AUTOANY&s={}&p={}'


def card_url(name, set=None):
    if set is None:
        set = ''
    return URL_BASE.format(uri_encode(set), uri_encode(name))


def price(name, set=None):
    url = card_url(name, set)
    html = get_html(url)
    xml = get_xml(html)
    product = xml.find('product')
    if product is None:
        return None
    return float(product.find('avgprice').text)


def prices(names, sets):
    urls = [card_url(n, s) for n, s in zip(names, sets)]
    htmls = get_htmls(urls)
    xmls = [get_xml(h) for h in htmls]
    products = [x.find('product') for x in xmls]
    for i in xrange(len(products)):
        if products[i] is not None:
            products[i] = float(products[i].find('avgprice').text)
    return products

real_sets = [
"Limited Edition Alpha",
"Limited Edition Beta",
"Unlimited Edition",
"Arabian Nights",
"Antiquities",
"Revised Edition",
"Legends",
"The Dark",
"Fallen Empires",
"Fourth Edition",
"Ice Age",
"Chronicles",
"Homelands",
"Alliances",
"Mirage",
"Visions",
"Fifth Edition",
"Portal",
"Weatherlight",
"Tempest",
"Stronghold",
"Exodus",
"Portal Second Age",
"Unglued",
"Urza's Saga",
"Urza's Legacy",
"Classic Sixth Edition",
"Urza's Destiny",
"Portal Three Kingdoms",
"Starter 1999",
"Mercadian Masques",
"Battle Royale Box Set",
"Nemesis",
"Starter 2000",
"Prophecy",
"Invasion",
"Beatdown Box Set",
"Planeshift",
"Seventh Edition",
"Apocalypse",
"Odyssey",
"Torment",
"Judgement",
"Onslaught",
"Legions",
"Scourge",
"Eighth Edition",
"Mirrodin",
"Darksteel",
"Fifth Dawn",
"Champions of Kamigawa",
"Unhinged",
"Betrayers of Kamigawa",
"Saviors of Kamigawa",
"Ninth Edition",
"Ravnica: City of Guilds",
"Guildpact",
"Dissension",
"Coldsnap",
"Time Spiral",
"Time Spiral \"Timeshifted\"",
"Planar Chaos",
"Future Sight",
"Tenth Edition",
"Lorwyn",
"Duel Decks: Elves vs. Goblins",
"Morningtide",
"Shadowmoor",
"Eventide",
"From the Vault: Dragons",
"Shards of Alara",
"Duel Decks: Jace vs. Chandra",
"Conflux",
"Duel Decks: Divine vs. Demonic",
"Alara Reborn",
"Magic 2010",
"From the Vault: Exiled",
"Planechase",
"Zendikar",
"Duel Decks: Garruk vs. Liliana",
"Premium Deck Series: Slivers",
"Worldwake",
"Duel Decks: Phyrexia vs. the Coalition",
"Rise of the Eldrazi",
"Archenemy",
"Magic 2011",
"From the Vault: Relics",
"Duel Decks: Elspeth vs. Tezzeret",
"Scars of Mirrodin",
"Premium Deck Series: Fire and Lightning",
"Mirrodin Besieged",
"Duel Decks: Knights vs. Dragons",
"New Phyrexia",
"Magic: The Gathering-Commander",
"Magic 2012",
"From the Vault: Legends",
"Duel Decks: Ajani vs. Nicol Bolas",
"Innistrad",
"Premium Deck Series: Graveborn",
"Dark Ascension",
"Duel Decks: Venser vs. Koth",
"Avacyn Restored",
"Planechase 2012 Edition",
"Magic 2013",
"From the Vault: Realms",
"Duel Decks: Izzet vs. Golgari",
"Return to Ravnica",
"Commander's Arsenal"
]

set_tests_1 = [
    ('Sphinx\'s Revelation', 'Return to Ravnica'),
    ('Bonfire of the Damned', 'Avacyn Restored'),
    ('Huntmaster of the Fells', 'Dark Ascension'),
    ('Geist of Saint Traft', 'Innistrad'),
    ('Karn Liberated', 'New Phyrexia'),
    ('Sword of Feast and Famine', 'Mirrodin Besieged'),
    ('Mox Opal', 'Scars of Mirrodin'),
    ('Kozilek, Butcher of Truth', 'Rise of the Eldrazi'),
    ('Jace, the Mind Sculptor', 'Worldwake'),
    ('Scalding Tarn', 'Zendikar'),
    ('Lord of Extinction', 'Alara Reborn'),
    ('Noble Hierarch', 'Conflux'),
    ('Elspeth, Knight-Errant', 'Shards of Alara'),
    ('Twilight Mire', 'Eventide'),
    ('Wilt-Leaf Liege', 'Shadowmoor'),
    ('Vendilion Clique', 'Morningtide'),
    ('Thoughtseize', 'Lorwyn'),
    ('Tarmogoyf', 'Future Sight'),
    ('Damnation', 'Planar Chaos'),
    ('Academy Ruins', 'Time Spiral'),
    ('Akroma, Angel of Wrath', 'Timeshifted'),
    ('Dark Depths', 'Coldsnap'),
    ('Breeding Pool', 'Dissension'),
    ('Godless Shrine', 'Guildpact'),
    ('Dark Confidant', 'Ravnica'),
    ('Erayo, Soratami Ascendant', 'Saviors of Kamigawa'),
    ('Umezawa\'s Jitte', 'Betrayers of Kamigawa'),
    ('Kiki-Jiki, Mirror Breaker', 'Champions of Kamigawa'),
    ('Crucible of Worlds', 'Fifth Dawn'),
    ('Sword of Fire and Ice', 'Darksteel'),
    ('Glimmervoid', 'Mirrodin'),
    ('Stifle', 'Scourge'),
    ('Akroma, Angel of Wrath', 'Legions'),
    ('Flooded Strand', 'Onslaught'),
]

set_tests_2 = [
    ('Burning Wish', 'Judgment'),
    ('Cabal Coffers', 'Torment'),
    ('Entomb', 'Odyssey'),
    ('Vindicate', 'Apocalypse'),
    ('Orim\'s Chant', 'Planeshift'),
    ('Phyrexian Altar', 'Invasion'),
    ('Plague Wind', 'Prophecy'),
    ('Kor Haven', 'Nemesis'),
    ('Rishadan Port', 'Mercadian Masques'),
    ('Rofellos, Llanowar Emissary', 'Urza\'s Destiny'),
    ('Grim Monolith', 'Urza\'s Legacy'),
    ('Gaea\'s Cradle', 'Urza\'s Saga'),
    ('City of Traitors', 'Exodus'),
    ('Mox Diamond', 'Stronghold'),
    ('Firestorm', 'Weatherlight'),
    ('Wasteland', 'Tempest'),
    ('Natural Order', 'Visions'),
    ('Lion\'s Eye Diamond', 'Mirage'),
    ('Force of Will', 'Alliances'),
    ('Baron Sengir', 'Homelands'),
    ('Necropotence', 'Ice Age'),
    ('Elvish Farmer', 'Fallen Empires'),
    ('Maze of Ith', 'The Dark'),
    ('Moat', 'Legends'),
    ('Mishra\'s Workshop', 'Antiquities'),
    ('Bazaar of Baghdad', 'Arabian Nights'),

    ('Thundermaw Hellkite', 'Magic 2013 (M13)'),
    ('Jace, Memory Adept', 'Magic 2012 (M12)'),
    ('Leyline of Sanctity', 'Magic 2011 (M11)'),
    ('Baneslayer Angel', 'Magic 2010 (M10)'),
    ('Crucible of Worlds', '10th Edition'),
    ('Lord of the Undead', '9th Edition'),
    ('Bribery', '8th Edition'),
    ('Wrath of God', '7th Edition'),
    ('Vampiric Tutor', 'Classic Sixth Edition'),
    ('Sylvan Library', 'Fifth Edition'),
    ('Land Tax', 'Fourth Edition'),
    ('Underground Sea', 'Revised Edition'),
    ('Black Lotus', 'Unlimited Edition'),
    ('Mox Jet', 'Beta Edition'),
    ('Underground Sea', 'Alpha Edition'),
    ('Nicol Bolas', 'From the Vault: Dragons'),
    ('Berserk', 'From the Vault: Exiled'),
    ('Kiki-Jiki, Mirror Breaker', 'From the Vault: Legends'),
    ('Ancient Tomb', 'From the Vault: Realms'),
    ('Mox Diamond', 'From the Vault: Relics')
]

set_tests_3 = [
    ('Lightning Helix', 'Duel Decks: Ajani vs. Nicol Bolas'),
    ('Demonic Tutor', 'Duel Decks: Divine vs. Demonic'),
    ('Tezzeret the Seeker', 'Duel Decks: Elspeth vs. Tezzeret'),
    ('Goblin Warchief', 'Duel Decks: Elves vs. Goblins'),
    ('Liliana Vess', 'Duel Decks: Garruk vs. Liliana'),
    ('Life from the Loam', 'Duel Decks: Izzet vs. Golgari'),
    ('Counterspell', 'Duel Decks: Jace vs. Chandra'),
    ('Knight of the Reliquary', 'Duel Decks: Knights vs Dragons'),
    ('Phyrexian Arena', 'Duel Decks: Phyrexia vs. the Coalition'),
    ('Path to Exile', 'Duel Decks: Venser vs. Koth'),
    ('Cabal Therapy', 'Premium Deck Series: Graveborn'),
    ('Coat of Arms', 'Premium Deck Series: Slivers'),
    ('Chain Lightning', 'Premium Deck Series: Fire and Lightning'),

    ('Flusterstorm', 'Commander'),
    ('Command Tower', 'Commander\'s Arsenal'),
    ('Thran Dynamo', 'Archenemy'),
    ('Tazeem', 'Planechase'),
    ('Blood Moon', 'Chronicles'),
    ('Natural Order', 'Portal'),
    ('Temporal Manipulation', 'Portal Second Age'),
    ('Imperial Seal', 'Portal Three Kingdoms'),
    ('Grim Tutor', 'Starter 1999'),
    ('Lava Axe', 'Starter 2000'),
    ('Land Tax', 'Battle Royale Box Set'),
    ('Ball Lightning', 'Beatdown Box Set'),
    ('Ashnod\'s Coupon', 'Unglued'),
    ('City of Ass', 'Unhinged'),
    ('Titania', 'Vanguard')
]


def load_tests(tests):
    names = [t[0] for t in tests]
    sets = [t[1] for t in tests]
    results = prices(names, sets)
    return zip(names, sets, results)


def run_tests(tests):
    for n, s, r in load_tests(tests):
        if r is None:
            print "FAILED: <{}> <{}> <{}>".format(n, s, card_url(n, s))


def run_all_tests():
    for tests in set_tests_1, set_tests_2, set_tests_3:
        run_tests(tests)


def print_sets():
    for tests in set_tests_1, set_tests_2, set_tests_3:
        for card, set in tests:
            print set
