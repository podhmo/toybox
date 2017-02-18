from ..shortcuts import _RunnerForOnefile
from ..simple import simple_view  # NOQA


def includeme(config):
    config.include(".jsonresponse")
    config.include("toybox.simple.simpleviews")
    config.add_simple_view_default_options({"renderer": "json"})


run = _RunnerForOnefile([lambda c: c.include(includeme)])
