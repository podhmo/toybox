def includeme_swagger_router(config):
    config.add_route('views', '/')
    config.add_route('views1', '/add')
    config.add_route('views2', '/dateadd')
    config.scan('.views')


def includeme(config):
    config.include(includeme_swagger_router)