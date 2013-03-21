from time import clock
from pyramid.settings import asbool
from mtgquery.lib.util import DEBUG

#Pages we don't want to do anything clever with
skip_exts = [
    'js',
    'css',
    'jpg',
    'png'
]


def skip_page(url):
    if url is None:
        return True
    return any('.'+ext in url for ext in skip_exts)


def simple_timer():
    start = clock()
    return lambda: clock() - start


def timing_tween_factory(handler, registry):
    if asbool(registry.settings.get('do_timing')):
        # if timing support is enabled, return a wrapper
        def timing_tween(request):
            timer = simple_timer()
            try:
                response = handler(request)
            finally:
                delta = timer()
                if not skip_page(request.url):
                    DEBUG('Loaded <{url}> in <{time}> seconds'.format(url=request.url, time=str(delta)))
            return response
        return timing_tween
    # if timing support is not enabled, return the original handler
    return handler
