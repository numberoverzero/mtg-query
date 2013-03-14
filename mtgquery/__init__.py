import os
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPMovedPermanently
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    sqlalchemy_url = os.environ.get('DATABASE_URL')
    settings['sqlalchemy.url'] = sqlalchemy_url

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    session_factory = UnencryptedCookieSessionFactoryConfig('alertsigner')
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('templates', 'templates', cache_max_age=3600)
    config.add_static_view('css', 'templates/css', cache_max_age=3600)
    config.add_static_view('js', 'templates/js', cache_max_age=3600)
    config.add_static_view('img', 'templates/img', cache_max_age=3600)
    config.add_static_view('cards', 'mtg_images/card_images', cache_max_age=3600)
    config.add_static_view('icons', 'mtg_images/icons', cache_max_age=3600)

    def add_auto_route(name, pattern, **kw):
        config.add_route(name, pattern, **kw)
        if not pattern.endswith('/'):
            config.add_route(name + '-auto', pattern + '/')

            def redirector(request):
                return HTTPMovedPermanently(request.route_url(name))
            config.add_view(redirector, route_name=name + '-auto')

    #####################################
    #
    #       HOME
    #
    #####################################
    add_auto_route('home', '/')

    #####################################
    #
    #       Help
    #
    #####################################

    # Help landing page
    add_auto_route('help', '/help')
    # Site help
    add_auto_route('help_site', '/help/site')
    # Markdown help
    add_auto_route('markdown_help', '/help/markdown')
    # Magic formatting help
    add_auto_route('magic_symbol_help', '/help/symbols')

    #####################################
    #
    #       Errors
    #
    #####################################

    add_auto_route('r403', '/403')
    add_auto_route('r404', '/404')
    add_auto_route('r500', '/500')

    #####################################
    #
    #       Synergy
    #
    #####################################

    #Submit
    add_auto_route('synergy_submit', '/submit')

    #Submit from copy
    add_auto_route('synergy_submit_copy', '/submit/from/{hash_id}')

    #View
    add_auto_route('synergy_view', '/{hash_id}')

    #View basic
    add_auto_route('synergy_view_basic', '/{hash_id}/basic')

    config.scan()
    return config.make_wsgi_app()
