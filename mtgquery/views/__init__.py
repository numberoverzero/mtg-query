from pyramid.view import view_config


def includeme(config):
    config.scan()


@view_config(route_name='home', renderer='mtgquery_base.mak')
def home(request):
    return {}
