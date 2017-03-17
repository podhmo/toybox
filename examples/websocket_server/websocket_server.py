import asyncio
import websockets


async def echo(websocket, path):
    if path == "/echo":
        while True:
            msg = await websocket.recv()
            await websocket.send(msg)
    else:
        msg = await websocket.recv()
        await websocket.send(msg)


def run_loop(port=6543):
    loop = asyncio.get_event_loop()
    start_server = websockets.serve(echo, 'localhost', port, loop=loop)
    loop.run_until_complete(start_server)
    loop.run_forever()


if __name__ == "__main__":
    run_loop(port=6543)
