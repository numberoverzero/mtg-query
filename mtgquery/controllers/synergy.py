from mtgquery.lib.synergy.submit_synergy import submit_new_synergy
from mtgquery.lib.synergy.load_synergy import load_existing_synergy
from mtgquery.lib.synergy.query import random_hash, newest_synergies


def create_synergy(cards, description, title):
    hash, notifications = submit_new_synergy(cards, title, description)
    return hash, notifications


def load_synergy(hash):
    view_count, urls, counts, title, description, form_dict = load_existing_synergy(hash)
    return urls, counts, title, description, form_dict


def get_random_hash():
    return random_hash()


def get_newest_synergyies():
    return newest_synergies(10)
