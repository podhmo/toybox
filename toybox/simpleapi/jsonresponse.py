import io
import traceback
from pyramid.events import NewRequest
from zope.interface import Interface


class IExceptionHandler(Interface):
    """handling exception"""
    def handle(request):
        pass


class ExceptionHandler(object):
    def handle(self, request):
        return {
            "code": "500 Internal Server Error",
            "title": "Internal Server Error",
            "message": str(request.exception),
            "traceback": self.get_traceback(request)
        }

    def get_traceback(self, request):
        return self.prettify(self._get_traceback(request))

    def _get_traceback(self, request):
        tbio = io.StringIO()
        traceback.print_exception(*request.exc_info, file=tbio)
        return tbio.getvalue()

    def prettify(self, message):
        return message.strip().split("\n")


def attach_http_accept_default(event):
    """Accept: application/json"""
    env = event.request.environ
    accept = env.get("HTTP_ACCEPT")
    if accept is None or "*/*":
        env["HTTP_ACCEPT"] = "application/json"


def exc_view(request):
    handler = request.registry.queryUtility(IExceptionHandler)
    if handler is None:
        handler = ExceptionHandler()
        request.registry.registerUtility(handler, IExceptionHandler)
    return handler.handle(request)


def includeme(config):
    config.add_view(view=exc_view, context=Exception, renderer="json")
    config.add_subscriber(attach_http_accept_default, NewRequest)
