from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from mtgquery.lib import notifications as Notifications
from mtgquery.lib.synergy.submit_synergy import submit_new_synergy
from mtgquery.lib.synergy.load_synergy import load_existing_synergy
from mtgquery.lib.synergy.query import random_hash, newest_synergies
from mtgquery.lib.util import merge_dicts


@view_config(route_name='synergy_submit', renderer='synergy/synergy_submit.mak')
def synergy_submit(request):
    if request.POST:
        return create_synergy(request)
    return {'navbar_index': 'Submit', 'form_name': '', 'form_description': '', 'form_cards_text': ''}


@view_config(route_name='synergy_submit_copy', renderer='synergy/synergy_submit.mak')
def synergy_submit_copy(request):
    if request.POST:
        return create_synergy(request)
    return merge_dicts({'navbar_index': 'Submit'}, load_synergy(request, False))


@view_config(route_name='synergy_view', renderer='synergy/synergy_view.mak')
def synergy_view(request):
    return merge_dicts({'navbar_index': 'View', 'view_mode': 'regular'}, load_synergy(request, False))


@view_config(route_name='synergy_view_basic', renderer='synergy/synergy_view.mak')
def synergy_view_basic(request):
    return merge_dicts({'view_mode': 'basic'}, load_synergy(request, True))


@view_config(route_name='synergy_random')
def synergy_random(request):
    hash = random_hash()
    if hash is None:
        url = request.route_url('r500')
    else:
        url = "/s/{}".format(hash)
    return HTTPFound(url)


@view_config(route_name='synergy_newest', renderer='synergy/synergy_newest.mak')
def synergy_newest(request):
    synergies = newest_synergies(10)
    return {'navbar_index': 'New', 'synergies': synergies}


@view_config(route_name='synergy_search', renderer='synergy/synergy_search.mak')
def synergy_search(request):
    return {'navbar_index': 'Search'}


def create_synergy(request):
    cards = request.POST['synergy-cards']
    description = request.POST['synergy-description']
    name = request.POST['synergy-name']
    hash_id, notifications = submit_new_synergy(cards, name, description)

    #Load notification messages up as strings
    for notification in notifications:
        Notifications.enqueue(notification, request.session)
    url = request.route_url('synergy_view', hash_id=hash_id)
    return HTTPFound(location=url)


def load_synergy(request, is_raw):
    hash_id = request.matchdict['hash_id']
    notifications = Notifications.load_from_flash(request.session)
    view_count, urls, counts, name, description, form_dict = load_existing_synergy(hash_id)
    alt_view = '/s/{}' if is_raw else '/s/{}/basic'  # Opposite view of the one we're loading
    return merge_dicts(form_dict, {'urls': urls, 'counts': counts,
                                   'name': name, 'description': description,
                                   'link_alt_href': alt_view.format(hash_id),
                                   'notifications': notifications,
                                   'copy_from_href': '/submit/from/{}'.format(hash_id)})
