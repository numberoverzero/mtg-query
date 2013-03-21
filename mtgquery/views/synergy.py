import mtgquery.controllers.synergy
from pyramid.view import view_config
from mtgquery.util import merge_dicts
from pyramid.httpexceptions import HTTPFound


@view_config(route_name='synergy_submit', renderer='synergy/synergy_submit.mak')
def synergy_submit(request):
    if request.POST:
        return create(request)
    return {'navbar_index': 'Submit', 'form_title': '', 'form_description': '', 'form_cards_text': ''}


@view_config(route_name='synergy_submit_copy', renderer='synergy/synergy_submit.mak')
def synergy_submit_copy(request):
    if request.POST:
        return create(request)
    return merge_dicts({'navbar_index': 'Submit'}, load(request, False))


@view_config(route_name='synergy_view', renderer='synergy/synergy_view.mak')
def synergy_view(request):
    return merge_dicts({'navbar_index': 'View', 'view_mode': 'regular'}, load(request, False))


@view_config(route_name='synergy_view_basic', renderer='synergy/synergy_view.mak')
def synergy_view_basic(request):
    return merge_dicts({'view_mode': 'basic'}, load(request, True))


@view_config(route_name='synergy_random')
def synergy_random(request):
    hash = mtgquery.controllers.synergy.get_random_hash()
    if hash:
        return HTTPFound('/s/' + hash)
    return request.route_url('r500')


@view_config(route_name='synergy_newest', renderer='synergy/synergy_newest.mak')
def synergy_newest(request):
    synergies = mtgquery.controllers.synergy.get_newest_synergyies()
    return {'navbar_index': 'New', 'synergies': synergies}


@view_config(route_name='synergy_search', renderer='synergy/synergy_search.mak')
def synergy_search(request):
    return {'navbar_index': 'Search'}


def create(request):
    cards = request.POST['synergy-cards']
    description = request.POST['synergy-description']
    title = request.POST['synergy-title']
    hash = mtgquery.controllers.synergy.create_synergy(cards, title, description)
    url = request.route_url('synergy_view', hash_id=hash)
    return HTTPFound(location=url)


def load(request, is_raw):
    hash = request.matchdict['hash_id']
    urls, counts, title, description, form_dict = mtgquery.controllers.synergy.load_synergy(hash)
    alt_view = '/s/{}' if is_raw else '/s/{}/basic'  # Opposite view of the one we're loading
    return merge_dicts(form_dict, {'urls': urls, 'counts': counts,
                                   'title': title, 'description': description,
                                   'link_alt_href': alt_view.format(hash),
                                   'notifications': [],
                                   'copy_from_href': '/submit/from/{}'.format(hash)})
