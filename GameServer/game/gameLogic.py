from wsClient import WebSocketClient
import asyncio
from sys import stderr
from typing import Type, List
import math

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
    def __init__(self, client, gameSet, game, userlist):
        self.client = client
        self.userlist = userlist
        self.game = game
        self.gameSet = gameSet
        self.players = []
        i = 1
        if gameSet["playeramount"] == 1:
            self.players.append(Player("1", "1", 0.2, 1))
            self.players.append(Player("2", "2", 0.2, 2))
        else:
            for user in userlist:
                self.players.append(Player(user, user, 0.2, i))
                i += 1
        self.initUser()
        self.plankdist = 0.45 # distance from middle to plank
        self.ball = Ball(float(gameSet["ballwidth"]), 0.006)
        print("Game logic set")


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
        for msg in messages:
            if len(msg) < 5:
                continue
            print(msg, file=stderr)
            if msg[0] == "1":
                print("P1", file=stderr)
                if msg[1] == "u":
                    print("up", file=stderr)
                    self.players[0].up = msg[4] == "n"
                    print("turn on: ",  msg[4] == "n", file=stderr)

                if msg[1] == "d":
                    self.players[0].down = msg[4] == "n"
            elif msg[0] == "2":
                if msg[1] == "u":
                    self.players[1].up = msg[4] == "n"
                if msg[1] == "d":
                    self.players[1].down = msg[4] == "n"

            elif msg[0] == "3":
                self.game["p3"] = self.doCmd(self.game["p3"], msg[1])
            elif msg[0] == "4":
                self.game["p4"] = self.doCmd(self.game["p4"], msg[1])
        # for message in messages:
        #     if message.endswith("login") and len(self.players) < self.gameSet["playeramount"]:
        #         player = self.getPlayer(message[:-5])
        #         if not player:
        #             continue
        #         player.connected = True
        #     else:
        #         commands.append({
        #             "token": message[:-1],
        #             "move":message[len(message) - 1:]})
        return commands

    def doCmd(self, p, data):

        if data == "u":
           return  0.025
        return -0.025

    async def gameInput(self):
        try:
            while True:
                commands = self.getMsgs()
                for command in commands:
                    player = self.getPlayer(command["token"])
                    if not player:
                        continue
                    player.move(command.move)
                for player in self.players:
                    player.update()
                    self.game["p1"] = self.players[0].plankPos
                    self.game["p2"] = self.players[1].plankPos
                    if len(self.players) == 4:
                        self.game["p3"] = self.players[2].plankPos
                        self.game["p4"] = self.players[3].plankPos
                self.ball.collide(self.players, self.plankdist)
                self.game["ballx"] = self.ball.pos["x"]
                self.game["bally"] = self.ball.pos["y"]
                if self.ball.game_over(-0.5, 0.5, -0.5, 0.5):
                    player = self.getPlayer(self.ball.last_touch)
                    if player:
                        self.game["score" + str(player.num)] += 1
                        if self.game["score"+ str(player.num)] >= int(self.gameSet["winpoint"]):
                            self.game["state"] = "game_over"
                            await self.client.sendMsg(self.game)
                            break
                    self.ball.reset()
                self.game["users"] = self.userlist
                await self.client.sendMsg(self.game)
                await asyncio.sleep(0.02)
                
        finally:
            print("GAME INPUT EXITED", file=stderr)


    def getPlayer(self, token):
        for player in self.players:
            if player.token == token:
                return player
        return 0

class Player:
    def __init__(self, username: str, token: str, plankLength: float, num:int):
        self.username = username
        self.plankPos = 0
        self.plankLength = plankLength
        self.token = token
        self.offset = 0.45
        self.connected = False
        self.upperBound = 100
        self.lowerBound = -100
        self.num = num
        self.collision = []
        self.speed = 0.025
        self.up = False
        self.down = False

    def update(self):
        if self.up:
            self.plankPos += self.speed
        if self.down:
            self.plankPos -= self.speed
        self.plankPos = min(self.plankPos, self.upperBound)
        self.plankPos = max(self.plankPos, self.lowerBound)
    
    def getPos(self):
        if self.num == 1:
            return {"x": -0.5, "y": self.plankPos}
        if self.num == 2:
            return {"x": 0.5, "y": self.plankPos}
        if self.num == 3:
            return {"x": self.plankPos, "y": -0.5}
        return {"x": self.plankPos, "y": 0.5}

class Ball:
    def __init__(self, size: float, speed: float):
        self.size = size
        self.pos = {"x": 0.0, "y": 0.0}
        self.speed = speed
        self.init_speed = speed
        self.dir = {"x": 1.0 , "y": 0.0 }
        self.c_a = 80
        self.last_touch = ""
        self.temp_last_touch = ""
    
    def reset(self):
        self.pos = {"x": 0.0, "y": 0.0}
        self.temp_last_touch = ""
        self.last_touch = ""
        self.speed = self.init_speed
    def game_over(self, x_min, x_max, y_min, y_max):
        return self.pos["x"] < x_min or self.pos["x"] > x_max or self.pos["y"] < y_min or self.pos["y"] > y_max
    
    def project_line(self, p1, p2, d1, d2, q1):
            if d1 == 0:
                return p2
            return (q1 - p1) / d1 * d2 + p2

    def dir_angle(self, angle):
        return {"x": math.cos(math.radians(angle)), "y": math.sin(math.radians(angle))}

    def dist(self, x1, y1, x2, y2):
        return pow(pow(x1 -x2, 2) + pow(y1 - y2, 2), 0.5)

    def seg_collide(self, p1, s1, p2, s2):
            if p1 > p2:
                return p1 - (s1 / 2) < p2 + (s2 / 2)
            return p2 - (s2 / 2) < p1 + (s1 / 2)

    def dir_wall(self, dir):
        return {"x": dir["x"], "y": -dir["y"]}

    def collide_paddle(self, px, py, s, p_dir, is_wall):
        if p_dir == "x": # paddle is like this: --
            p_c = self.project_line(self.pos["y"], self.pos["x"], self.dir["y"], self.dir["x"], py)
            c_pos = {"x": p_c, "y": py} # collision position
            if not self.seg_collide(p_c, self.size, px, s):
                return -1, 0, 0
            # down, y dir positive
            new_dir = self.dir_angle(self.c_a * (p_c - px) / s + 90)
            # up, y dir negative
            if self.dir["y"] > 0:
                    new_dir = self.dir_angle(self.c_a * (p_c - px) / s + 270)    
            if is_wall:
                new_dir = self.dir_wall(self.dir)
            dist = self.dist(p_c, py, self.pos["x"], self.pos["y"])
            return dist, new_dir, c_pos
        # paddle is like this: |  
        p_c = self.project_line(self.pos["x"], self.pos["y"], self.dir["x"], self.dir["y"], px) # find the y coordinate of the intersection point
        c_pos = {"x": px, "y": p_c}
        # print("collide is ", self.seg_collide(p_c, self.size, py, s), " as collide point is ", p_c, "yet plank point is ", py, file=stderr)
        if not self.seg_collide(p_c, self.size, py, s): # verify that the y coordinate is on the paddle
            return -1, 0, 0
        
        # right, x dir positive
        new_dir = self.dir_angle(180 + (self.c_a * (py - p_c) / s))
        # left, x dir negative
        if self.dir["x"] < 0:
            new_dir = self.dir_angle(self.c_a * (p_c - py) / s)
        # dist from ball to paddle
        dist = self.dist(px, p_c, self.pos["x"], self.pos["y"])
        return dist, new_dir, c_pos

    def collide_horz_wall(self, py):
        return self.collide_paddle(-1, py, 10, "x", True)

    def set_if_smaller(self, newCol, last_touch):
        if newCol[0] != -1 and newCol[0] < self.collision[0]:
            self.collision = newCol
            self.temp_last_touch = last_touch

    def collide(self, players: List[Player], plankdist: float):
        remaining_dist = self.speed
        self.temp_last_touch = ""
        while (remaining_dist > 0):
            self.collision = [math.inf, {}, {}]
            # print("Players", len(players), file=stderr)
            if (self.dir["x"] > 0 and len(players) > 1): # moving right, can hit right player (2)
                self.set_if_smaller(self.collide_paddle(players[1].offset, players[1].plankPos, players[1].plankLength, "y", False), players[1].token)
            if (self.dir["x"] < 0 and len(players) > 0): # moving left, can hit left player (1)
                self.set_if_smaller(self.collide_paddle(-players[0].offset, players[0].plankPos, players[0].plankLength, "y", False), players[0].token)
            if (self.dir["y"] > 0): # moving down, can hit bottom player (4)
                if len(players) > 2:
                    self.set_if_smaller(self.collide_paddle(players[3].plankPos, players[3].offset, players[3].plankLength, "x", False), players[3].token)
                else:
                    self.set_if_smaller(self.collide_horz_wall(0.5), "")
            if (self.dir["y"] < 0): # moving up, can hit top player (3)
                if len(players) > 2:
                    self.set_if_smaller(self.collide_paddle(players[2].plankPos, -players[2].offset, players[2].plankLength, "x", False), players[2].token)
                else:
                    self.set_if_smaller(self.collide_horz_wall(-0.5), "")
            # there is a collision. There can be a new collision
            if self.collision[0] >= 0 and self.collision[0] < remaining_dist:
                self.dir = self.collision[1]
                self.pos = self.collision[2]
                remaining_dist -= self.collision[0]
                # print("COLLIDE FOUND", file=stderr)
                # print("dist remaining", remaining_dist, file=stderr)
                if self.temp_last_touch != "":
                    self.last_touch = self.temp_last_touch
                if self.speed < 2:
                    self.speed *= 1.2
            else:
            # there is no collision within range
                self.pos["x"] += self.dir["x"] * remaining_dist
                self.pos["y"] += self.dir["y"] * remaining_dist
                remaining_dist = 0