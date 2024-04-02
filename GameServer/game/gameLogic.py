from wsClient import WebSocketClient
import asyncio
from sys import stderr
from typing import Type, List

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
        self.players = []
        self.initUser()
        self.plankdist = 0.45 # distance from middle to plank


    def print(self, msg):
        print(YELLOW,"Game logic :", msg, RESET, file=stderr)


    def initUser(self):
        i = 1
        # while i <= 4:
        #     if self.gameSet[("user" + str(i))]:
        #         self.users.append(self.gameSet[("user" + str(i))])
        #     i += 1


    def getMsgs(self):
        messages = self.client.getMsg()
        if not messages:
            return []
        commands = []
        for message in messages:
            if message.endswith("login") and len(self.players) < self.gameSet["playeramount"]:
                player = self.getPlayer(message[:-5])
                if not player:
                    continue
                player.connected = True
            else:
                commands.append({
                    "token": message[:-1],
                    "move":message[len(message) - 1:]})
        return commands


    async def gameInput(self):
        try:
            while True:
                commands = self.getMsgs()
                for command in commands:
                    player = self.getPlayer(command.token)
                    if not player:
                        continue
                    player.move(command.move)
                await self.client.sendMsg(self.game)
                await asyncio.sleep(0.1)
        finally:
            print("GAME INPUT EXITED", file=stderr)


    def getPlayer(self, token):
        for player in self.players:
            if player.token == token:
                return player
        return 0

class Player:
    def __init__(self, username: str, token: str, plankLength: float, num:int, num_players:int):
        self.username = username
        self.plankPos = 0
        self.plankLength = plankLength
        self.token = token
        self.offset = 1
        self.connected = False
        self.upperBound = 100
        self.lowerBound = -100
        self.num = num
        self.num_players = num_players

    def move(self, command):
        if command == 'u':
            self.plankPos += self.offset
        elif command == 'd':
            self.plankPos -= self.offset
        self.plankPos = min(self.plankPos, self.upperBound)
        self.plankPos = max(self.plankPos, self.lowerBound)
    
    def getPos(self):
        if self.num == 1:
            return {"x": -0.5, "y": self.plankPos}
        if self.num == 2 and self.num_players == 4:
            return {"x": self.plankPos, "y": -0.5}
        if self.num == 2 or self.num == 3:
            return {"x": 0.5, "y": self.plankPos}
        return {"x": self.plankPos, "y": 0.5}

class Ball:
    def __init(self, size: float, speed: float):
        self.size = size
        self.speed = speed
        self.pos = {"x": 0.0, "y": 0.0}
        self.dir = {"x": 1.0, "y": 0.0}

    def update(self, players: List[Player], plankdist: float):
        pass

    def get_update(self):
        return {"x": self.pos["x"] + (self.dir["x"] * self.speed),
     "y": self.pos["y"] + self.dir["y"] * self.speed}
    
    def collide(self, players: List[Player], plankdist: float):
        x_offset = plankdist
        y_offset = 0.5
        n_pos = self.get_update()
        if (len(players) == 4):
            y_offset = plankdist
        if (n_pos["x"] > x_offset):
            pass # check player 2 (2 player) or player 3 (4 player)
        if (n_pos["x"] < -x_offset):
            pass # check player 1
        if (n_pos["y"] < -y_offset):
            pass # hit wall (2 player) or player 2 (4 player)
        if (n_pos["y"] > y_offset):
            pass # hit wall (2 player) or player 4 (4 player)
        



# specify side or specify position?
