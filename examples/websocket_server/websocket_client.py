#!/usr/bin/env python

import asyncio
import websockets

async def communicate(ws, prefix=None):
    for i in range(5):
        await ws.send(str(i))
        print("{}: > {}".format(prefix, i))

        msg = await ws.recv()
        print("{}: < {}".format(prefix, msg))


async def hello():
    async with websockets.connect('ws://localhost:6543/echo') as ws:
        await asyncio.wait([communicate(ws, prefix="@"), communicate(ws, prefix="#")])

asyncio.get_event_loop().run_until_complete(hello())
