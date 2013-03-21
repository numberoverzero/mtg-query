from pyramid.view import view_config, forbidden_view_config, notfound_view_config
from mtgquery.controllers.synergy import SynergyHashNotFoundException
from mtgquery.util import get_logger
from mtgquery.controllers.error import error_data
import traceback

log = get_logger(__name__)


@forbidden_view_config(renderer='error.mak')
def forbidden(request):
    log.info("403 Forbidden <{}>".format(request.url))
    request.response.status_int = 403
    return error_data('403')


@notfound_view_config(renderer='error.mak')
def notfound(request):
    log.info("404 NotFound <{}>".format(request.url))
    request.response.status_int = 404
    return error_data('404')


@view_config(context=Exception, renderer='error.mak')
def catch_all(exception, request):
    es = str(exception)
    tb = traceback.format_exc()
    log.error(es + '\n' + tb)
    request.response.status_int = 500
    return error_data('500')


@view_config(context=SynergyHashNotFoundException, renderer='error.mak')
def synergy_not_found(exception, request):
    request.response.status_int = 404
    response = error_data('404hash')
    response['line2'] = response['line2'].format(exception.hash)
    return response
