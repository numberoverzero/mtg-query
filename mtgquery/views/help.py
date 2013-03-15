from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from mtgquery.lib import help as Help


@view_config(route_name='help', renderer='help.mak')
def help(request):
    return HTTPFound('/help/site')


@view_config(route_name='help_site', renderer='help.mak')
def help_site(request):
    contents = Help.basic_contents
    return {'navbar_index': 'Help', 'contents': contents}


@view_config(route_name='markdown_help', renderer='help.mak')
def markdown_help(request):
    contents = Help.text_contents
    return {'navbar_index': 'Help', 'contents': contents}


@view_config(route_name='magic_symbol_help', renderer='help.mak')
def magic_symbol_help(request):
    contents = Help.magic_symbols
    return {'navbar_index': 'Help', 'contents': contents}
