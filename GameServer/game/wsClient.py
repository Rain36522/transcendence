import asyncio
import websockets

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.messages = []

    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def receive_messages(self):
        async for message in self.websocket:
            self.messages.append(message)

    """Client to game serv
    char 0 = player number
    char 1 : u = up, d = down
    """
    def getMsg(self):
        import json
        msg = []
        for message in self.messages:
            msg.append((message[0], message[1]))
        self.messages.clear()
        return msg

    async def sendMsg(self, msg):
        import json
        await self.websocket.send(json.dumps(msg))


