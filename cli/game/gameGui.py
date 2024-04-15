
from os import system
from game.DataTransmission import DataTransmission
from color import *
from ascii import Ascii
from blessed import Terminal
from time import sleep
import asyncio



# contexte = {
#         "nbPlayers": player,
#         "paddleWidth": 0.02,
#         "paddleLength": game.planksize,
#         "paddleOffset": 0.02,
#         "ballSize": game.ballwidth,
#         "isSolo": solo,
#         "status": "waiting",
#         "user": request.user.username,
#         "gameid": id
#     }


class GameGui2p:
    def __init__(self, settings, wsCli):
        print("START", settings)
        self.term = Terminal()
        self.wsCli = wsCli
        self.settings = settings
        self.pos = 0.5
        self.putNewMap()
        if settings["isSolo"]:
            self.userpose = 1
        else:
            self.userpose = 0

    """MAP
    Map generation in CLI.
    Calculing the max size of map. Kipping litel space for score.
    """
    async def updateGame(self):
        while True:
            await asyncio.sleep(0.03)
            msg = self.wsCli.getMessage()
            if str(msg).isdigit():
                return msg
            elif msg:
                if str(msg["state"]) == "game_over":
                    return msg
                elif not self.userpose and self.settings["user"] in msg["users"]:
                    if msg["users"][0] == self.settings["user"]:
                        self.userpos = 1
                    else:
                        self.userpose = 2
                if self.userpose == 2:
                    msg = self.updateMsg(msg, revers=-1)
                    self.updatePaddelL(msg["p2"])
                    self.updatePaddelR(msg["p1"])
                else:
                    msg = self.updateMsg(msg)
                    self.updatePaddelL(msg["p1"])
                    self.updatePaddelR(msg["p2"])
                self.updateBall(msg["ballx"], msg["bally"])
    
    def updateMsg(self, msg, revers=1):
        liste = ["ballx", "bally", "p1", "p2"]
        for elem in liste:
                msg[elem] = (msg[elem] * revers) + 0.5
        return msg


    def putNewMap(self):
        system("clear")
        self.GetMapSize()
        self.putMap()
        print(BYELLOW)
        self.putPaddel(self.pos, 1)
        print(RESET)
        self.putPaddel(0.5, self.width)
        self.getBallPos(0.5, 0.5)
        self.putBall()
        sleep(0.3)


    def GetMapSize(self):
        
        self.column = self.term.width
        self.line = self.term.height - 5
        
        self.width = 0
        self.height = 0
        while self.height < self.line - 4 and self.width < self.column - 7:
            self.width += 4
            self.height += 1
        if self.width >= self.column - 4:
            self.start = 0
        else:
            self.start = (self.column - self.width) // 2
        self.padelsize = self.settings["paddleLength"] * self.height
        self.ballsize = self.settings["ballSize"] * self.height
        if round(self.padelsize) % 2 != self.height % 2:
            self.padelsize += 1
        if round(self.ballsize) % 2 != self.height % 2:
            self.ballsize += 1
        print(self.padelsize, self.ballsize, self.height)
    
    def putMap(self):
        print(self.term.move_xy(0, 3), end="")
        i = 0
        print(BBLUE + " " * self.start + "+" + "-" * self.width + "+", end="\n\r")
        while i < self.height:
            print(" " * self.start + "|" + " " * self.width + "|", end="\n\r")
            i += 1
        print(" " * self.start + "+" + "-" * self.width + "+" + RESET, end="\n\r")
    
    def calculateNewPaddelPos(self, newPos):
        start = round(self.height * newPos - self.padelsize / 2)
        stop = round(start + self.padelsize)
        return start, stop

    def putPaddel(self, posy, posx):
        start, stop = self.calculateNewPaddelPos(posy)
        self.padelLu = start
        self.padelLd = stop
        self.padelRu = start
        self.padelRd = stop
        while start < stop:
            self.putCharInMap(posx, start, "█")
            start += 1

    def updatePaddelL(self, newPos):
        print(BYELLOW)
        start, stop = self.calculateNewPaddelPos(newPos)
        while start < self.padelLu and self.padelLu > 0:
            self.putCharInMap(1, self.padelLu, "█")
            self.padelLu -= 1
        while start > self.padelLu:
            self.putCharInMap(1, self.padelLu, " ")
            self.padelLu += 1
        while stop < self.padelLd:
            self.putCharInMap(1, self.padelLd, " ")
            self.padelLd -= 1
        while stop > self.padelLd and self.padelLd < self.height + 1:
            self.putCharInMap(1, self.padelLd, "█")
            self.padelLd += 1
        print(RESET)
    
    def updatePaddelR(self, newPos):
        start, stop = self.calculateNewPaddelPos(newPos)
        while start < self.padelRu and self.padelRu > 0:
            self.putCharInMap(self.width, self.padelRu, "█")
            self.padelRu -= 1
        while start > self.padelRu:
            self.putCharInMap(self.width, self.padelRu, " ")
            self.padelRu += 1
        while stop < self.padelRd:
            self.putCharInMap(self.width, self.padelRd, " ")
            self.padelRd -= 1
        while stop > self.padelRd and self.padelRd < self.height + 1:
            self.putCharInMap(self.width, self.padelRd, "█")
            self.padelRd += 1


    def getBallPos(self, posx, posy):
        self.ballx = round(self.width * posx - self.ballsize)
        self.bally = round(self.height * posy - self.ballsize / 2)
    

    def putBall(self, char="█"):
        stopx = round(self.ballx + self.ballsize * 2)
        stopy = round(self.bally + self.ballsize)
        if self.ballx <= 1:
            self.ballx = 2
        elif stopx >= self.width:
            stopx = self.width - 1
        if self.bally <= 0:
            self.bally = 1
        elif stopy > self.height + 1:
            stopy = self.height + 1
        if char == "█":
            print(ORANGE)
        y = self.bally
        while y < stopy:
            i = self.ballx
            while i < stopx:
                self.putCharInMap(i, y, char)
                i += 1
            y += 1
        if char == "█":
            print(RESET)
        
    def updateBall(self, posx, posy):
        self.putBall(" ")
        self.getBallPos(posx, posy)
        self.putBall()

        

    def putCharInMap(self, posx, posy, charToPut):
        posx += self.start + 0
        posy += 4
        print(self.term.move_xy(posx, posy) + str(charToPut))
