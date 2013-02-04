
from pyramid.settings import asbool
from lib import skip_page
from mtgquery.lib.util import DEBUG, simple_timer

# Commented out until we can remove the hack
#from bs4 import BeautifulSoup
from ..UGLY_HACKS import bs4_hacked_prettify


def __beautify(url, response):
    t = simple_timer()

    raw_text = response.text
    #soup = BeautifulSoup(raw_text)
    #pretty_soup = soup.prettify()

    #HACK  #HACK  #HACK  #HACK  #HACK  #HACK  #HACK  #HACK  #HACK  #HACK  #HACK
    pretty_soup = bs4_hacked_prettify(raw_text)

    response.text = pretty_soup

    DEBUG("Beautified <{}> in <{}> seconds".format(url, t()))


def htmlbeautify_tween_factory(handler, registry):
    if asbool(registry.settings.get('do_beautify')):
        # if html beautify is enabled, return a wrapper
        def htmlbeautify_tween(request):
            response = handler(request)
            if not skip_page(request.url):
                __beautify(request.url, response)
            return response
        return htmlbeautify_tween
    # if html beautify support is not enabled, return the original handler
    return handler
