import sys
import transaction

##########################
#
#
# Loads card data from a sqlite database.
# The card data should be generated from the Gatherer Downloader.
#
#
##########################

from mtgquery.models import Card as RealCard
from mtgquery.models import (
    DBSession,
    CardArtist,
    CardCost,
    CardFlavorText,
    CardName,
    CardOracleRules,
    CardPrintedName,
    CardPrintedRules,
    CardPrintedType,
    CardRarity,
    CardSet,
    CardType,
    CardWatermark
    )
from mtgquery.models import get_or_create
from mtgquery.scripts import gen_help_links

from mtgquery.lib.http import get_htmls
from mtgquery.lib.util import make_sure_path_exists
from mtgquery.lib import gatherer_icons

dstSession = DBSession()
load_model = lambda model, **kwargs: get_or_create(dstSession, model, **kwargs)

import sqlsoup
import itertools


def load_cards_from(db_path):
    sql_db_name = 'sqlite:///{}'.format(db_path.replace('\\', '/'))
    srcDB = sqlsoup.SQLSoup(sql_db_name)
    srcDB.execute("select 1").scalar()
    srcCards = srcDB.MTGCardInfo.all()
    total = len(srcCards)
    next_warn = 0
    for i, card in enumerate(srcCards):
        if int(100. * i / total) >= next_warn:
            print "{0}% done".format(next_warn)
            next_warn += 1
        load_card(card)


def load_card(srcCard):
    multiverse_id = srcCard.id
    number = srcCard.cardnum
    power = srcCard.power
    toughness = srcCard.toughness
    card = RealCard(
        multiverse_id=multiverse_id,
        number=number,
        power=power,
        toughness=toughness,
        )

    card.artist = load_model(CardArtist, artist=srcCard.artist)
    card.cost = load_model(CardCost, cost=srcCard.cost)
    card.flavor_text = load_model(CardFlavorText, flavor_text=srcCard.flavor)
    card.name = load_model(CardName, name=srcCard.name)
    card.oracle_rules = load_model(CardOracleRules, oracle_rules=srcCard.rules)
    card.printed_name = load_model(CardPrintedName, printed_name=srcCard.printedname)
    card.printed_rules = load_model(CardPrintedRules, printed_rules=srcCard.printedrules)
    card.printed_type = load_model(CardPrintedType, printed_type=srcCard.printedtype)
    card.rarity = load_model(CardRarity, rarity=srcCard.rarity)
    card.set = load_model(CardSet, set=srcCard.set)
    card.type = load_model(CardType, type=srcCard.type)
    card.watermark = load_model(CardWatermark, watermark=srcCard.watermark)

    dstSession.add(card)

src_path = """http://gatherer.wizards.com/Handlers/Image.ashx?size={}&name={}&type=symbol"""
root_dst_folder = """D:\\Workspace\\PythonWorkspace\\mtg_env\\mtgquery\\mtgquery\\mtg_images\\icons"""


def save_icon(size, name, data):
    loc = root_dst_folder + "\\" + size
    make_sure_path_exists(loc)
    filename = loc + "\\{}.jpg".format(name)
    with open(filename, 'wb') as f:
        f.write(data)


def load_mtg_icons():
    good_icons = []
    urls = []
    for icon in itertools.product(gatherer_icons.sizes, gatherer_icons.icons):
        if icon in gatherer_icons.skip:
            print "SKIPPING: {} {}".format(*icon)
            continue
        url = src_path.format(*icon)
        urls.append(url)
        good_icons.append(icon)
    print "Loading data..."
    datas = get_htmls(urls)
    print "Loaded data!"
    print "Saving data..."
    for icon, data in zip(good_icons, datas):
        save_icon(icon[0], icon[1], data)
    print "Saved data!"

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 2:
        sys.exit(1)
    db_path = argv[1]
    load_cards_from(db_path)
    gen_help_links.main()
    transaction.commit()
    load_mtg_icons()
