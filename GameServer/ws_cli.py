import asyncio
import websockets

async def hello():
    uri = "ws://127.0.0.1:8001/gameid/user"
    async with websockets.connect(uri) as websocket:
        i = 0
        await websocket.send("Hello world")
        message_received = await websocket.recv()
        print("Message reçu :", message_received)
        print("close")
    await websocket.close()

asyncio.get_event_loop().run_until_complete(hello())
