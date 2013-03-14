import traceback
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, forbidden_view_config, notfound_view_config

from mtgquery.lib import exceptions
from mtgquery.lib import help as Help
from mtgquery.lib import notifications as Notifications
from mtgquery.lib.synergy.submit_synergy import submit_new_synergy
from mtgquery.lib.synergy.load_synergy import load_existing_synergy
from mtgquery.lib.util import merge_dicts, INFO, ERROR
import error_info


@view_config(route_name='r403', renderer='basic_error.mak')
def v403(request):
    request.response.status_int = 403
    return error_info.error('403')


@view_config(route_name='r404', renderer='basic_error.mak')
def v404(request):
    request.response.status_int = 404
    return error_info.error('404')


@view_config(route_name='r500', renderer='basic_error.mak')
def v500(request):
    request.response.status_int = 500
    return error_info.error('500')


@forbidden_view_config(renderer='basic_error.mak')
def forbidden(request):
    INFO("403 Forbidden <{}>".format(request.url))
    request.response.status_int = 403
    return error_info.error('403')


@notfound_view_config(renderer='basic_error.mak')
def notfound(request):
    INFO("404 NotFound <{}>".format(request.url))
    request.response.status_int = 404
    return error_info.error('404')


@view_config(context=Exception, renderer='basic_error.mak')
def catch_all(exception, request):
    es = str(exception)
    tb = traceback.format_exc()
    ERROR(es + '\n' + tb)
    request.response.status_int = 500
    return error_info.error('500')


@view_config(context=exceptions.SynergyHashNotFoundException, renderer='basic_error.mak')
def synergy_not_found(exception, request):
    request.response.status_int = 404
    response = error_info.error('404hash')
    response['line1'] = response['line1'].format('synergies')
    response['line2'] = response['line2'].format('synergy', exception.hash)
    return response


@view_config(route_name='home', renderer='mtgquery_base.mak')
def home(request):
    return {}


@view_config(route_name='synergy', renderer='synergy/synergy_submit.mak')
def synergy(request):
    if request.POST:
        return redirect_new_synergy(request)
    return {'navbar_index': 'Synergy'}


@view_config(route_name='synergy_copy_from', renderer='synergy/synergy_submit.mak')
def synergy_copy_from(request):
    return load_synergy(request, False)


@view_config(route_name='synergy_load', renderer='synergy/synergy_load.mak')
def synergy_load(request):
    if request.POST:
        return redirect_new_synergy(request)
    return load_synergy(request, False)


@view_config(route_name='synergy_load_raw', renderer='synergy/synergy_view_raw.mak')
def synergy_load_raw(request):
    return load_synergy(request, True)


@view_config(route_name='help', renderer='help/basic.mak')
def help(request):
    return HTTPFound('/help/site')


@view_config(route_name='help_site', renderer='help/basic.mak')
def help_site(request):
    contents = Help.basic_contents
    return {'navbar_index': 'Help', 'contents': contents}


@view_config(route_name='markdown_help', renderer='help/basic.mak')
def markdown_help(request):
    contents = Help.text_contents
    return {'navbar_index': 'Help', 'contents': contents}


@view_config(route_name='magic_symbol_help', renderer='help/basic.mak')
def magic_symbol_help(request):
    contents = Help.magic_symbols
    return {'navbar_index': 'Help', 'contents': contents}


def redirect_new_synergy(request):
    cards = request.POST['synergy-cards']
    description = request.POST['synergy-description']
    name = request.POST['synergy-name']
    hash_id, notifications = submit_new_synergy(cards, name, description)

    #Load notification messages up as strings
    for notification in notifications:
        Notifications.enqueue(notification, request.session)
    url = request.route_url('synergy_load', hash_id=hash_id)
    return HTTPFound(location=url)


def load_synergy(request, is_raw):
    hash_id = request.matchdict['hash_id']
    notifications = Notifications.load_from_flash(request.session)
    view_count, urls, counts, name, description, form_dict = load_existing_synergy(hash_id)
    href = '/synergy/{}' if is_raw else '/synergy/raw/{}'
    return merge_dicts(form_dict, {'navbar_index': 'Synergy',
                                   'urls': urls, 'counts': counts,
                                   'name': name, 'description': description,
                                   'link_alt_href': href.format(hash_id),
                                   'notifications': notifications,
                                   'copy_from_href': href.format('from/' + hash_id)})
