import websockets
import asyncio
import os
import sys

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = [set(), {}, {}] # self.clients contain the differents connexion (django, game instance, user)
        self.clients
    
    async def handle_client(self, websocket, path):
        msg = []
        if path == "/":
            await self.DjangoMsg(websocket, path)
        elif path.startswith("/game/"):
            await self.GameMsg(websocket, path)
        elif path.startswith("/wsGame/"):
            await self.UserMsg(websocket, path)

    async def start_server(self):
        print("Server is runing in : " + self.host + ":" + str(self.port), file=sys.stderr)
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()

    def run(self):
        asyncio.create_task(self.start_server())
    
        """Django msg manage.
        communication between django server and game serveur
        path = /
        save as list.
        """
    async def DjangoMsg(self, websocket, path):
        self.clients[0].add(websocket)
        print("New django connection", file=sys.stderr)
        try:
            async for message in websocket:
                self.execDjangoMsg(message)
        finally:
            print("django is disconnected", file=sys.stderr)
            self.clients[0].remove(websocket)

    def execDjangoMsg(self, msg):
        os.environ["newGame"] = msg # add json string in env
        os.system("python3 game/game.py &") # launch game instance. detached mode
    
    """game communication:
    Communication between game instance.
    Save as map (gameid, client)
    """
    async def GameMsg(self, websocket, path):
        print("New game connection", file=sys.stderr)
        gameid = path[6:]
        self.clients[1][gameid] = websocket
        try:
            async for message in websocket:
                await self.execGameMsg(message, gameid)
        finally:
            print("game client is disconnected", file=sys.stderr)
            del self.clients[1][gameid]

    async def execGameMsg(self, message, gameid):
        if gameid in self.clients[2]:
            for cli in self.clients[2][gameid]:
                await cli[1].send(message)

        """User msg
        Communication between server and client.
        Saved as map (gameid, vector of client.)
        """
    async def UserMsg(self, websocket, path):
        print("New User connection", file=sys.stderr)
        path = path.split("/")
        while "" in path:
            path.remove("")
        if len(path) != 3:
            return
        gameid = path[1]
        user = path[2]
        self.addUser(websocket, gameid, user)
        try:
            async for message in websocket:
                await self.execUserMsg(message, gameid, user)
        finally:
            #send to game instance user disconnected.
            print("user disconnect", file=sys.stderr)
            if gameid in self.clients[1]:
                await self.clients[1][gameid].send((user + "disconnected"))
            self.rmUser(websocket, gameid)

    def addUser(self, websocket, gameid, user):
        find = False
        if gameid in self.clients[2]:
            self.clients[2][gameid].add((user, websocket))
            find = True
        if not find:
            newset = set()
            newset.add((user, websocket))
            self.clients[2][gameid] = newset
    
    def rmUser(self, websocket, gameid):
        if gameid in self.clients[2]:
            for user in self.clients[2][gameid]:
                if user[1] == websocket:
                    self.clients[2][gameid].discard(user)
                    break
            if not len(self.clients[2][gameid]):
                del self.clients[2][gameid]


    async def execUserMsg(self, message, gameid, user):
        if gameid in self.clients[1]:
            await self.clients[1][gameid].send((user + message))

async def main():
    # os.system("python3 game/game.py &") # launch game instance. detached mode
    ws = WebSocketServer("0.0.0.0", 8001)
    ws.run()
    while True:
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
