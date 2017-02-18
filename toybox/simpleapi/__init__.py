from toybox.simple.simpleviews import simple_view  # NOQA


def includeme(config):
    config.include(".jsonresponse")
    config.include("toybox.simple.simpleviews")
    config.add_simple_view_default_options({"renderer": "json"})
