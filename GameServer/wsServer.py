import websockets
import asyncio
import os

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = [set(), set(), set()] # self.clients contain the differents connexion (django, game instance, user)
        self.clients
    
    async def handle_client(self, websocket, path):
        msg = []
        if path == "/":
            await self.DjangoMsg(websocket, path)
        elif path.startswith("/ws/game/"):
            self.clients[1].add(websocket)
            await self.GameMsg(websocket, path)
        elif path.startswith("/ws/"):
            await self.UserMsg(websocket, path)
        self.clients.add(websocket)
        # print("path :", path)
        # print(websocket.remote_address[0])
        # for client in self.clients:
        #     await client.send(websocket.remote_address[0])
        try:
            async for message in websocket:
                msg.append(message)
        finally:
            print("close connection")
            self.clients.remove(websocket)

    async def start_server(self):
        print("Server is runing in : " + self.host + ":" + str(self.port))
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()

    def run(self):
        asyncio.create_task(self.start_server())
    

    async def DjangoMsg(self, websocket, path):
        self.clients[0].add(websocket)
        try:
            async for message in websocket:
                self.execDjangoMsg(message)
        finally:
            self.clients[0].remove(websocket)

    def execDjangoMsg(self, msg):
        if msg.startswith("newgame "):
            print("os.system")
    
    #path = /game/gameid
    async def GameMsg(self, websocket, path):
        self.clients[1].add(websocket)
        try:
            async for message in websocket:
                self.execGameMsg(message)
        finally:
            self.clients[1].remove(websocket)

    def execGameMsg(self, message):


    async def UserMsg(self, websocket, path):
        path = path.split("/")
        gameid = path[0]
        user = path[1]
        if len(path) == 2:
            self.addUser(websocket, path)
    
    def addUser(self, websocket, path):
        path = path.split("/")
        find = False
        if len(path) == 3:
            for i in self.client[2]:
                if i[0] == path[1]:
                    i[1].add(path[2])
                    find = True
                    break
            if not find:
                newset = set()
                newset.add(path[2])
                self.clients[2].add((path[1], newset))


async def main():
    ws = WebSocketServer("0.0.0.0", 8001)
    ws.run()
    while True:
        await asyncio.sleep(0.02)

if __name__ == "__main__":
    asyncio.run(main())
