from wsClient import WebSocketClient
import asyncio
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

"""
login / logout
"""

class gameLogic:
    def __init__(self, client, gameSet, game):
        self.client = client
        self.game = game
        self.gameSet = gameSet
        self.user = []
        self.initUser()
    
    def print(self, msg):
        print(YELLOW,"Game logic :", msg, RESET, file=stderr)


    def initUser(self):
        if self.gameSet["user1"]:
            self.user.append(self.gameSet["user1"])
        if self.gameSet["user2"]:
            self.user.append(self.gameSet["user2"])
        if self.gameSet["user3"]:
            self.user.append(self.gameSet["user3"])
        if self.gameSet["user4"]:
            self.user.append(self.gameSet["user4"])

    """Client to game serv
    char 0 = player number
    char 1 : u = up, d = down
    """
    def getMsgs(self):
        messages = self.client.getMsg()
        if messages:
            msg = []
            for message in messages:
                if message.endswith("login") and len(self.user) < self.gameSet["playeramount"] and message[:-5] not in self.user:
                    self.print("New user " + message[:-5])
                    self.user.append(message[:-5])
                else:
                    for user in self.user:
                        if message.startswith(user):
                            msg.append(message[len(user):])
                            break
            return msg
        return None



    async def sendMsg(self):
        await self.client.sendMsg(self.game)

    async def gameInput(self):
        try:
            i = False
            while True:
                messages = self.getMsgs()
                if messages:
                    for msg in messages:
                        self.print(messages)
                        if msg[0] == "1":
                            self.game["p1"] = self.doCmd(self.game["p1"], msg[1])
                        elif msg[0] == "2":
                            self.game["p2"] = self.doCmd(self.game["p2"], msg[1])
                        elif msg[0] == "3":
                            self.game["p3"] = self.doCmd(self.game["p3"], msg[1])
                        elif msg[0] == "4":
                            self.game["p4"] = self.doCmd(self.game["p4"], msg[1])
                if i:
                    self.game["ballx"] = 10
                    self.game["bally"] = 10
                    i = False
                else:
                    self.game["ballx"] = 0
                    self.game["bally"] = 0
                    i = True
                await self.sendMsg()
                await asyncio.sleep(0.1)
        finally:
            print("GAME INPUT EXCITED", file=stderr)
                    
            
    
    def doCmd(self, p, data):
        if data == "u":
            p += 1
        elif data == "d":
            p -= 1
        return p
