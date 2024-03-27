import websockets
import asyncio
import os
from sys import stderr

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
ORANGE = "\033[38;2;255;165;0m"

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = [set(), {}, {}] # self.clients contain the differents connexion (django, game instance, user)
        self.finishGames = []

    def print(self, msg):
        print(BLUE,"Game Server :", msg, RESET, file=stderr)
    
    async def handle_client(self, websocket, path):
        msg = []
        if path.startswith("/game/"):
            await self.GameMsg(websocket, path)
        elif path.startswith("/wsGame/"):
            await self.UserMsg(websocket, path)

    async def start_server(self):
        async with websockets.serve(self.handle_client, self.host, self.port):
            self.print(GREEN + "Server is runing in : " + self.host + ":" + str(self.port))
            await asyncio.Future()

    def run(self):
        asyncio.create_task(self.start_server())

    def getDjangoMsg(self):
        if not self.finishGames:
            return None
        msg = self.finishGames.copy()
        self.finishGames.clear()
        return msg
    
    """game communication:
    Communication between game instance.
    Save as map (gameid, client)
    """
    async def GameMsg(self, websocket, path):
        self.print("New game connection")
        gameid = path[6:]
        self.clients[1][gameid] = websocket
        try:
            async for message in websocket:
                await self.execGameMsg(message, gameid)
        finally:
            self.print("game client is disconnected")
            del self.clients[1][gameid]

    async def execGameMsg(self, message, gameid):
        if message.startswith("finish"):
            self.finishGames.append(message[6:])
        elif gameid in self.clients[2]:
            for cli in self.clients[2][gameid]:
                await cli[1].send(message)

        """User msg
        Communication between server and client.
        Saved as map (gameid, vector of client.)
        """
    async def UserMsg(self, websocket, path):
        self.print("New User connection")
        path = path.split("/")
        while "" in path:
            path.remove("")
        if len(path) != 3:
            return
        gameid = path[1]
        user = path[2]
        if gameid not in self.clients[1]:
            self.print(ORANGE + "Wrong game id")
            websocket.send(404)
            return
        self.addUser(websocket, gameid, user)
        await self.clients[1][gameid].send((user + "connected"))
        try:
            async for message in websocket:
                await self.execUserMsg(message, gameid, user)
        finally:
            #send to game instance user disconnected.
            self.print("user disconnected", file=stderr)
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
