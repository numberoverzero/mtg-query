from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPMovedPermanently
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config
import controllers
import os

from .models import (
    Base,
    DBSession,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # Connect DB
    sqlalchemy_url = os.environ.get('DATABASE_URL')
    settings['sqlalchemy.url'] = sqlalchemy_url
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    # Preheat any cached data
    if settings['preheat_cache'] == 'true':
        controllers.preheat_cache()

    session_factory = UnencryptedCookieSessionFactoryConfig('alertsigner')
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('templates', 'templates', cache_max_age=3600)
    config.add_static_view('css', 'css', cache_max_age=3600)
    config.add_static_view('js', 'js', cache_max_age=3600)
    config.add_static_view('cards', 'mtg_images/card_images', cache_max_age=3600)
    config.add_static_view('icons', 'mtg_images/icons', cache_max_age=3600)

    def add_auto_route(name, pattern, **kw):
        config.add_route(name, pattern, **kw)
        if not pattern.endswith('/'):
            config.add_route(name + '-auto', pattern + '/')

            def redirector(request):
                return HTTPMovedPermanently(request.route_url(name))
            config.add_view(redirector, route_name=name + '-auto')

    add_auto_route('home', '/')
    add_auto_route('r403', '/403')
    add_auto_route('r404', '/404')
    add_auto_route('r500', '/500')

    # Help landing page
    add_auto_route('help', '/help')
    # Site help
    add_auto_route('help_site', '/help/site')
    # Markdown help
    add_auto_route('markdown_help', '/help/markdown')
    # Magic formatting help
    add_auto_route('magic_symbol_help', '/help/symbols')

    #Submit
    add_auto_route('synergy_submit', '/submit')
    #Submit from copy
    add_auto_route('synergy_submit_copy', '/submit/from/{hash_id}')
    #View
    add_auto_route('synergy_view', '/s/{hash_id}')
    #View basic
    add_auto_route('synergy_view_basic', '/s/{hash_id}/basic')
    #Random
    add_auto_route('synergy_random', '/random')
    #New
    add_auto_route('synergy_newest', '/new')
    #Search
    add_auto_route('synergy_search', '/search')

    config.include('mtgquery.views')
    return config.make_wsgi_app()
