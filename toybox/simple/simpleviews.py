import venusian
from pyramid.config import PHASE1_CONFIG, PHASE0_CONFIG
from pyramid.interfaces import IDict
from ..langhelpers import normalize


PRIORITY_LOW = -10
PRIORITY_NORMAL = 0
PRIORITY_HIGH = 10


class ISimpleViewOptionsDefault(IDict):
    pass


def _get_registered_routes(config, k="toybox.simpleapi.registered"):
    if k not in config.registry.settings:
        config.registry.settings[k] = set()
    return config.registry.settings[k]


# from: http://madjar.github.io/europython2013/#/step-1
def add_simple_view(config, view, path, *args, **kwargs):
    def callback():
        # xxx:
        registered = _get_registered_routes(config)

        route_name = kwargs.pop("route_name", None) or normalize(path)
        if route_name not in registered:
            config.add_route(route_name, path)
            registered.add(route_name)

        default_kwargs = config.registry.queryUtility(ISimpleViewOptionsDefault)
        if default_kwargs is None:
            new_kwargs = kwargs
        else:
            default_kwargs.pop("_priority", None)
            new_kwargs = default_kwargs.copy()
            new_kwargs.update(kwargs)
        config.add_view(view, route_name=route_name, *args, **new_kwargs)

    discriminator = ('add_simple_view', path, kwargs.get("request_method"), kwargs.get("context"))
    config.action(discriminator, callback, order=PHASE1_CONFIG)


def add_simple_view_default_options(config, default, priority=PRIORITY_NORMAL):
    default["_priority"] = priority

    def callback():
        value = config.registry.queryUtility(ISimpleViewOptionsDefault)
        if value is None:
            config.registry.registerUtility(default, ISimpleViewOptionsDefault)
        elif value["_priority"] < priority:
            config.registry.registerUtility(default, ISimpleViewOptionsDefault)

    discriminator = ('simple_view_options_default', priority)
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
