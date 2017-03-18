from .decorator import withswagger  # NOQA
from .renderers import ValidatedJSON


def includeme(config):
    # xxx:
    config.add_renderer('json', ValidatedJSON())
