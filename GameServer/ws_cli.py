import asyncio
import websockets

async def hello():
    uri = "ws://127.0.0.1:8000/"
    async with websockets.connect(uri) as websocket:
        print("connected")
        await websocket.send("newgame Hello world")
        print("close")
    await websocket.close()

asyncio.get_event_loop().run_until_complete(hello())
