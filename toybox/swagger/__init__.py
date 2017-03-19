from .decorator import withswagger  # NOQA
from .renderers import ValidatedJSON


def simpleapi(config):
    config.include(includeme)
    config.include("toybox.simpleapi")
    config.add_simple_view_default_options({"renderer": "vjson"})


def includeme(config):
    config.add_renderer('vjson', ValidatedJSON())
