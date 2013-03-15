from pyramid.view import view_config, forbidden_view_config, notfound_view_config
from mtgquery.lib.synergy import SynergyHashNotFoundException
from mtgquery.lib.util import INFO, ERROR
import traceback


@view_config(route_name='r403', renderer='error.mak')
def v403(request):
    request.response.status_int = 403
    return error('403')


@view_config(route_name='r404', renderer='error.mak')
def v404(request):
    request.response.status_int = 404
    return error('404')


@view_config(route_name='r500', renderer='error.mak')
def v500(request):
    request.response.status_int = 500
    return error('500')


@forbidden_view_config(renderer='error.mak')
def forbidden(request):
    INFO("403 Forbidden <{}>".format(request.url))
    request.response.status_int = 403
    return error('403')


@notfound_view_config(renderer='error.mak')
def notfound(request):
    INFO("404 NotFound <{}>".format(request.url))
    request.response.status_int = 404
    return error('404')


@view_config(context=Exception, renderer='error.mak')
def catch_all(exception, request):
    es = str(exception)
    tb = traceback.format_exc()
    ERROR(es + '\n' + tb)
    request.response.status_int = 500
    return error('500')


@view_config(context=SynergyHashNotFoundException, renderer='error.mak')
def synergy_not_found(exception, request):
    request.response.status_int = 404
    response = error('404hash')
    response['line1'] = response['line1'].format('synergies')
    response['line2'] = response['line2'].format('synergy', exception.hash)
    return response


_images = {
    '404hash': {
        'line1': "These aren't the {} you're looking for.",
        'line2': "(We couldn't find the {} hash {})",
        'img': "404hash.png"
    },
    '404': {
        'line1': "I have no idea what you were trying to find.",
        'line2': "(We've alerted the proper authorities)",
        'img': "404.png"
    },
    '403': {
        'line1': "Nice try, pal.",
        'line2': "(You're not authorized to view that)",
        'img': "403.png"
    },
    '500': {
        'line1': "Something's gone wrong.  We're.... working on it.",
        'line2': "(The people responsible have been lit on fire)",
        'img': "500.png"
    },

}

# Use cloudinary CDN
url = 'http://res.cloudinary.com/mtg-query/image/upload/{}'
for image_dict in _images.values():
    image_dict['img'] = url.format(image_dict['img'])


def error(string):
    if string in _images:
        return dict(_images[string])
    return None
