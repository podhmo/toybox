import asyncio
import websockets
from zope.interface import Interface, Attribute
from multiprocessing import Process
from toybox.simple import simple_view, run


class IExternalProcessHandler(Interface):
    uri = Attribute("uri")
    process = Attribute("process")


async def echo(websocket, path):
    if path == "/echo":
        while True:
            msg = await websocket.recv()
            await websocket.send(msg)
    else:
        msg = await websocket.recv()
        await websocket.send(msg)


@simple_view("/", renderer="index.html")
def home(request):
    handler = request.registry.getUtility(IExternalProcessHandler)
    return {"handler": handler}


def include_forking_ws_server(config):
    def run_loop():
        loop = asyncio.get_event_loop()
        start_server = websockets.serve(echo, 'localhost', 6543, loop=loop)
        loop.run_until_complete(start_server)
        loop.run_forever()

    class Handler:
        process = Process(target=run_loop)
        uri = "ws://localhost:6543"

    # todo: more comfortable handling
    Handler.process.start()
    config.registry.registerUtility(Handler, IExternalProcessHandler)


def include_renderer_settings(config):
    config.include("pyramid_mako")
    config.add_mako_renderer(".html")
    # "websocket_server" is package name (this file's name)
    config.add_static_view(name='static', path='websocket_server:static', cache_max_age=0)


if __name__ == "__main__":
    import logging
    import os.path

    logging.basicConfig(level=logging.DEBUG)
    here = os.path.dirname(os.path.abspath(__file__))
    settings = {
        "mako.directories": here,
        "pyramid.reload_all": True
    }
    run.include(include_renderer_settings)
    run.include(include_forking_ws_server)
    run(port=8080, settings=settings)
