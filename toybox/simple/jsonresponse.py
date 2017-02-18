import io
import traceback
from pyramid.events import NewRequest


def attach_http_accept_default(event):
    """Accept: application/json"""
    env = event.request.environ
    accept = env.get("HTTP_ACCEPT")
    if accept is None or "*/*":
        env["HTTP_ACCEPT"] = "application/json"


def exc_view(request):
    tbio = io.StringIO()
    traceback.print_exception(*request.exc_info, file=tbio)
    return {"message": str(request.exception), "traceback": tbio.getvalue()}


def includeme(config):
    config.add_view(view=exc_view, context=Exception, renderer="json")
    config.add_subscriber(attach_http_accept_default, NewRequest)
