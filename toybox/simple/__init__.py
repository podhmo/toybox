from ..shortcuts import _RunnerForOnefile
from .simpleviews import simple_view  # NOQA
from .simpleviews import (PRIORITY_LOW, PRIORITY_NORMAL, PRIORITY_HIGH)  # NOQA


def includeme(config):
    config.include(".simpleviews")

run = _RunnerForOnefile([includeme])
