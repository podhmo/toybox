import venusian
from pyramid.config import PHASE1_CONFIG


# from: http://madjar.github.io/europython2013/#/step-1
def add_simple_view(config, view, path, *args, **kwargs):
    def callback():
        route_name = view.__qualname__
        config.add_route(route_name, path)
        config.add_view(view, route_name=route_name, *args, **kwargs)
    discriminator = ('add_simple_view', path)
    config.action(discriminator, callback, order=PHASE1_CONFIG)


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
