from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from mtgquery.controllers.help import load_html


@view_config(route_name='help', renderer='help.mak')
def help_main(request):
    return HTTPFound('/help/site')


@view_config(route_name='help_site', renderer='help.mak')
def help_site(request):
    contents = load_html('site')
    return {'navbar_index': 'Help', 'contents': contents}


@view_config(route_name='markdown_help', renderer='help.mak')
def markdown_help(request):
    contents = load_html('markdown')
    return {'navbar_index': 'Help', 'contents': contents}


@view_config(route_name='magic_symbol_help', renderer='help.mak')
def magic_symbol_help(request):
    contents = load_html('symbols')
    return {'navbar_index': 'Help', 'contents': contents}
