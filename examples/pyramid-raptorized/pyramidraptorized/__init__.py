from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramidraptorized.models import initialize_sql

import raptorizemw

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'pyramidraptorized:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_view('pyramidraptorized.views.my_view',
                    route_name='home',
                    renderer='templates/mytemplate.pt')
    app = config.make_wsgi_app()
    app = raptorizemw.make_middleware(app)
    return app

