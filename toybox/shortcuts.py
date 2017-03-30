import sys
from functools import partial
from pyramid.config import Configurator
from pyramid.path import caller_package


def cont_wsgi(config, host="0.0.0.0", port=8080, make_server=None, cont=lambda server: server.serve_forever()):
    if make_server is None:
        from wsgiref.simple_server import make_server
    app = config.make_wsgi_app()
    print("running host={!r}, port={!r}".format(host, port), file=sys.stderr)
    server = make_server(host, port, app)
    return cont(server)


def cont_pshell(config):
    from code import interact
    config.commit()
    return interact("", local={"config": config, "registry": config.registry})


def cont_proutes(config):
    from pyramid.scripts.proutes import get_route_data
    config.commit()
    mapper = config.get_routes_mapper()
    routes = mapper.get_routes(include_static=True)
    for route in routes:
        route_data = get_route_data(route, config.registry)
        for name, pattern, view, method in route_data:
            print(name, pattern, view, method)


def cont_ptweens(config):
    from pyramid.interfaces import ITweens
    from pyramid.tweens import INGRESS, MAIN

    def show_chain(chain):
        fmt = '%-10s  %-65s'
        print(fmt % ('Position', 'Name'))
        print(fmt % ('-' * len('Position'), '-' * len('Name')))
        print(fmt % ('-', INGRESS))
        for pos, (name, _) in enumerate(chain):
            print(fmt % (pos, name))
        print(fmt % ('-', MAIN))

    tweens = config.registry.queryUtility(ITweens)
    if tweens is not None:
        print('"pyramid.tweens" config value set '
              '(explicitly ordered tweens used)')
        print('')
        print('Explicit Tween Chain (used)')
        print('')
        show_chain(tweens.explicit)
        print('')
        print('Implicit Tween Chain (not used)')
        print('')
        show_chain(tweens.implicit())


class _RunnerForOnefile(object):
    """don't use this in production"""

    def __init__(self, modifiers=None):
        self.modifiers = modifiers or []

    def include(self, modify):
        self.modifiers.append(modify)
        return self

    @property
    def wsgi(self):
        return partial(self.__call__, cont=cont_wsgi)

    @property
    def handle_request(self):
        return partial(self.__call__, cont=partial(cont_wsgi, cont=lambda s: s.handle_request()))

    @property
    def pshell(self):
        return partial(self.__call__, cont=cont_pshell)

    @property
    def proutes(self):
        return partial(self.__call__, cont=cont_proutes)

    @property
    def ptweens(self):
        return partial(self.__call__, cont=cont_ptweens)

    def __call__(self, settings=None, debug=True, cont=cont_wsgi, scan=True, package=None, level=2, *args, **kwargs):
        package = package or caller_package(level=level)
        config = Configurator(package=package, settings={"debug_all": debug, **settings})

        for callable in self.modifiers:
            config.include(callable)

        if scan:
            scan_point = package.__name__
            print("scanning {}".format(scan_point), file=sys.stderr)
            config.scan(scan_point)

        return cont(config, *args, **kwargs)
