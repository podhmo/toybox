import sys
from pyramid.config import Configurator
from pyramid.path import caller_package
from wsgiref.simple_server import make_server


class _RunnerForOnefile(object):
    """don't use this in production"""

    def __init__(self, modifiers=None):
        self.modifiers = modifiers or []

    def add_modify(self, modify):
        self.modifiers.append(modify)

    def __call__(self, host="0.0.0.0", port=8080, make_server=make_server, modifiers=None, scan=True, package=None, level=2):
        package = package or caller_package(level=level)

        config = Configurator(package=package)
        for modify in self.modifiers:
            modify(config)
        for modify in modifiers or []:
            modify(config)
        app = config.make_wsgi_app()

        scan_point = None
        if scan:
            scan_point = package.__name__
            config.scan(scan_point)

        print("running host={!r}, port={!r}, scan={!r}".format(host, port, scan_point), file=sys.stderr)
        server = make_server(host, port, app)
        return server.serve_forever()
