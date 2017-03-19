from ..shortcuts import _RunnerForOnefile
from ..simple import simple_view, PRIORITY_LOW  # NOQA


def includeme(config):
    config.include(".jsonresponse")
    config.include("toybox.simple.simpleviews")
    config.add_simple_view_default_options({"renderer": "json"}, priority=PRIORITY_LOW)


run = _RunnerForOnefile([includeme])
