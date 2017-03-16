from ..shortcuts import _RunnerForOnefile
from .simpleviews import simple_view  # NOQA


def includeme(config):
    config.include(".simpleviews")

run = _RunnerForOnefile([includeme])
