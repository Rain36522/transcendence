import asyncio
import ssl
import websockets

async def hello():
    uri = "wss://127.0.0.1:443/wsGame"
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        i = 0
        await websocket.send("Hello world")
        print("Message send")
        message_received = await websocket.recv()
        print("Message reçu :", message_received)
        print("close")

asyncio.get_event_loop().run_until_complete(hello())
