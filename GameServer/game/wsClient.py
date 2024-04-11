import asyncio
import websockets
from sys import stderr


class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.messages = []

    async def connect(self):
        self.websocket = await websockets.connect(self.url)
        print("Game instance connected to", self.url, file=stderr)

    async def receive_messages(self):
        try:
            async for message in self.websocket:
                self.messages.append(message)
        finally:
            print("Game instance disconnected to", self.url, file=stderr)

    """Client to game serv
    char 0 = player number
    char 1 : u = up, d = down
    """
    def getMsg(self):
        msg = []
        for message in self.messages:
            msg.append(message)
        self.messages.clear()
        return msg

    async def sendMsg(self, msg):
        import json
        await self.websocket.send(json.dumps(msg))
        if msg["state"] == "game_over":
            await self.websocket.close()
            exit(0)


