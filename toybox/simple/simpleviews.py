import venusian
from pyramid.config import PHASE1_CONFIG, PHASE0_CONFIG
from pyramid.interfaces import IDict
from ..langhelpers import normalize


class ISimpleViewOptionsDefault(IDict):
    pass


# from: http://madjar.github.io/europython2013/#/step-1
def add_simple_view(config, view, path, registered=set(), *args, **kwargs):
    def callback():
        route_name = normalize(path)
        if route_name not in registered:
            config.add_route(route_name, path)
            registered.add(route_name)

        default_kwargs = config.registry.queryUtility(ISimpleViewOptionsDefault)
        if default_kwargs is None:
            new_kwargs = kwargs
        else:
            new_kwargs = default_kwargs.copy()
            new_kwargs.update(kwargs)
        config.add_view(view, route_name=route_name, *args, **new_kwargs)

    discriminator = ('add_simple_view', path, kwargs.get("request_method"), kwargs.get("context"))
    config.action(discriminator, callback, order=PHASE1_CONFIG)


def add_simple_view_default_options(config, default):
    def callback():
        config.registry.registerUtility(default, ISimpleViewOptionsDefault)
    discriminator = ('simple_view_options_default', )
    config.action(discriminator, callback, order=PHASE0_CONFIG)


class simple_view(object):
    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.args = args
        self.kwargs = kwargs

    def register(self, scanner, name, wrapped):
        scanner.config.add_simple_view(wrapped, self.path, *self.args, **self.kwargs)

    def __call__(self, wrapped):
        venusian.attach(wrapped, self.register)
        return wrapped


def includeme(config):
    config.add_directive("add_simple_view", add_simple_view)
    config.add_directive("add_simple_view_default_options", add_simple_view_default_options)
