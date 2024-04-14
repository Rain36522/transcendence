import sys
import os
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_parent)
from game.DataTransmission import DataTransmission
from color import *
from ascii import Ascii
from blessed import Terminal
import asyncio

gameSettings = {
    "ballwidth" : 0.1, #max size plank size calculation
    "planksize" : 0.3, #max size 50%
    "Speed" : 0.01,
    "acceleration" : 0.01, #increase speed each bounce
    "playeramount" : 2,
    "winpoint" : 10,
    "user1" : "",
    "user2" : "",
    "user3" : "",
    "user4" : ""
}

#add minimal screen size = width 40, height 20
class GameGui2p:
    def __init__(self, settings, wsCli):
        self.term = Terminal()
        self.wsCli = wsCli
        self.settings = settings
        os.system("clear")
        self.GetMapSize()
        self.putMap()
        self.height -= 2
        self.width -= 2
        if settings["isSolo"]:
            self.userpos = 1
        else:
            self.userpose = 0
        self.initPadelL()
        self.initPadelR()
        self.initBall()
    

    async def  updateGame(self):
        while True:
            await asyncio.sleep(0.03)
            msg = self.wsCli.getMessage()
            if msg:
                if msg["state"] == "game_over":
                    return msg
                elif not self.userpose and self.settings["user"] in msg["users"]:
                    if msg["users"][0] == self.settings["user"]:
                        self.userpos = 1
                    else:
                        self.userpos = 2
                if self.userpos == 2:
                    msg = self.updateMsg(msg, reverse=-1)
                    self.updatePadelL(msg["p2"])
                    self.updatePadelR(msg["p1"])
                else:
                    msg = self.updateMsg(msg)
                    self.updatePadelL(msg["p1"])
                    self.updatePadelR(msg["p2"])
                self.updateBall(msg["ballx"], msg["bally"])
    
    def updateMsg(self, msg, reverse=1):
        liste = ["ballx", "bally", "p1", "p2"]
        for elem in liste:
                msg[elem] = msg[elem] * reverse + 0.5
        return msg

    """MAP
    Map generation in CLI.
    Calculing the max size of map. Kipping litel space for score.
    """
    def GetMapSize(self):
        
        self.column = self.term.width // 2
        self.line = self.term.height - 3
        
        print("Terminal width :", self.column, "height :", self.line, end="\n\r")
        
        self.width = 0
        self.height = 0
        while self.height < self.line - 1 and self.width < self.column - 2:
            self.width += 2
            self.height += 1
        if self.width >= self.column:
            self.start = 0
        else:
            self.start = self.column - self.width
        for cle, value in self.settings.items():
            print(cle, ":", value)
        self.padelsize = self.settings["paddleLength"] * self.height
        self.ballsize = self.settings["ballSize"] * self.height
    
    def putMap(self):
        print(self.term.move_xy(0, 3))
        self.skipStart()
        print("+", end="")
        print(("--" * (self.width - 2)) + "+", end="\n\r")
        for i in range(self.height - 2):
            self.skipStart()
            print("|", end="")
            print("  " * (self.width - 2), end="")
            print("|", end="\n\r")
        self.skipStart()
        print("+", end="")
        print("--" * (self.width - 2) + "+")
    """Paddels
    Put the paddel.
    When there is an padel update, we just change the padel pos by adding paddel or space char.
     We only erase and put again in case of padel totaly outside of the actual padel.
    """
    def calculPaddels(self, pos=-1):
        if pos == -1:
            midelpoint = self.height / 2 + 4
        else:
            midelpoint = pos * self.height + 3
        high = round(midelpoint + self.padelsize / 2)
        low = round(midelpoint - self.padelsize / 2)
        return low, high
    
    def initPadelL(self):
        self.padelL = {}
        low, high = self.calculPaddels()
        self.padelL["x"] = self.start + 1
        self.padelL["low"] = low
        self.padelL["high"] = high

        j = self.padelL["low"]
        while j < self.padelL["high"]:
            print(self.term.move_xy(self.padelL["x"], j) + "█")
            j += 1
    
    def initPadelR(self):
        self.padelR = {}
        low, high = self.calculPaddels()
        self.padelR["x"] = self.start + self.width * 2
        self.padelR["low"] = low
        self.padelR["high"] = high
        j = self.padelR["low"]
        while j < self.padelR["high"]:
            print(self.term.move_xy(self.padelR["x"], j) + "█")
            j += 1

    def updatePadelL(self, padelpos):
        low, high = self.calculPaddels(padelpos)
        if abs(self.padelL["low"] - low) > self.padelsize: #padel totaly change
            self.changePadel(self.padelL["x"], self.padelL["high"], self.padelL["low"], " ")
            self.changePadel(self.padelL["x"], high, low, "█")
            self.padelL["low"] = low
            self.padelL["high"] = high
            return

        if self.padelL["low"] > low: # case of padel go down
            self.changePadel(self.padelL["x"], self.padelL["low"], low, "█")
            self.padelL["low"] = low
        elif self.padelL["low"] < low:
            self.changePadel(self.padelL["x"], low, self.padelL["low"], " ")
            self.padelL["low"] = low
        
        if self.padelL["high"] > high: # case of padel go up
            self.changePadel(self.padelL["x"], self.padelL["high"], high, " ")
            self.padelL["high"] = high
        elif self.padelL["high"] < high:
            self.changePadel(self.padelL["x"], high, self.padelL["high"], "█")
            self.padelL["high"] = low
        
    def updatePadelR(self, padelpos):
        low, high = self.calculPaddels(padelpos)
        if abs(self.padelR["low"] - low) > self.padelsize: #padel totaly change
            self.changePadel(self.padelR["x"], self.padelR["high"], self.padelR["low"], " ")
            self.changePadel(self.padelR["x"], high, low, "█")
            self.padelR["low"] = low
            self.padelR["high"] = high
            return
        
        if self.padelR["low"] > low: # case of padel go down
            self.changePadel(self.padelR["x"], self.padelR["low"], low, "█")
            self.padelR["low"] = low
        elif self.padelR["low"] < low:
            self.changePadel(self.padelR["x"], low, self.padelR["low"], " ")
            self.padelR["low"] = low
        
        if self.padelR["high"] > high: # case of padel go up
            self.changePadel(self.padelR["x"], self.padelR["high"], high, " ")
            self.padelR["high"] = high
        elif self.padelR["high"] < high:
            self.changePadel(self.padelR["x"], high, self.padelR["high"], "█")
            self.padelR["high"] = low

        
    def changePadel(self, xpos, stop, start, char):
        if start < 4:
            start = 4
        if stop > self.height + 5:
            stop = self.height + 5
        j = start
        while j < stop:
            print(self.term.move_xy(xpos, j) + char)
            j += 1
    
    """Ball
    Calculating the ball size. depending the ball size remove and add in new position.
    """

    def calculBall(self, balx, baly):
        balx = balx * self.width
        baly = baly * self.height
        return round(balx - self.ballsize), round(baly - self.ballsize / 2)

    
    def initBall(self):
        self.ball = {}
        self.ball["x"], self.ball["y"] = self.calculBall(1, 0.5)
        self.putBall(self.ball["x"], self.ball["y"], "█")

    def updateBall(self, posx, posy):
        x, y = self.calculBall(posx, posy)
        if self.ball["x"] != x or self.ball["y"] != y:
            self.putBall(self.ball["x"], self.ball["y"], " ")
            self.putBall(x, y, "█")
            self.ball["x"] = x
            self.ball["y"] = y


    def putBall(self, x, y, char):
        y += 4
        x += self.start + 1
        j = y
        while j < y + round(self.ballsize):
            print(self.term.move_xy(x, j) + char * round(self.ballsize) * 2)
            j += 1
    
    def skipStart(self):
        if self.start:
            print(" " * self.start, end="")
