from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("toybox.simple")
    config.scan(".views")
    return config.make_wsgi_app()
