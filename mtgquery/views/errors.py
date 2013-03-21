from pyramid.view import view_config, forbidden_view_config, notfound_view_config
from mtgquery.lib.synergy import SynergyHashNotFoundException
from mtgquery.lib.util import INFO, ERROR
from mtgquery.controllers.error import error_data
import traceback


@forbidden_view_config(renderer='error.mak')
def forbidden(request):
    INFO("403 Forbidden <{}>".format(request.url))
    request.response.status_int = 403
    return error_data('403')


@notfound_view_config(renderer='error.mak')
def notfound(request):
    INFO("404 NotFound <{}>".format(request.url))
    request.response.status_int = 404
    return error_data('404')


@view_config(context=Exception, renderer='error.mak')
def catch_all(exception, request):
    es = str(exception)
    tb = traceback.format_exc()
    ERROR(es + '\n' + tb)
    request.response.status_int = 500
    return error_data('500')


@view_config(context=SynergyHashNotFoundException, renderer='error.mak')
def synergy_not_found(exception, request):
    request.response.status_int = 404
    response = error_data('404hash')
    response['line2'] = response['line2'].format(exception.hash)
    return response
