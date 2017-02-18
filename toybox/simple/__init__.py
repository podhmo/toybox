from .simpleviews import simple_view  # NOQA


def includeme(config):
    config.include(".simpleviews")
    config.include(".jsonresponse")
