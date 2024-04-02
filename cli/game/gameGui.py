import sys
import os
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_parent)

from color import *
from ascii import Ascii
from time import sleep
from blessed import Terminal

class GameGui2p:
    def __init__(self):
        self.term = Terminal()
        os.system("clear")
        self.GetMapSize()
        self.putMap()
        sleep(1)

    def GetMapSize(self):
        
        self.column = self.term.width // 2
        self.line = self.term.height - 3
        
        print("Terminal width :", self.column, "height :", self.line, end="\n\r")
        
        self.width = 0
        self.height = 0
        while self.height < self.line + 1 and self.width < self.column + 2:
            self.width += 2
            self.height += 1
        if self.width + 2 >= self.column:
            self.start = 0
        else:
            self.start = self.column - self.width
        print("width :", self.width, "height :", self.height, end="\n\r")
    
    def putMap(self):
        print(self.term.move_xy(0, 3))
        self.skipStart()
        print(" ", end="")
        print("##" * (self.width - 2), end="\n\r")
        for i in range(self.height - 2):
            self.skipStart()
            print("#", end="")
            print("  " * (self.width - 2), end="")
            print("#", end="\n\r")
        self.skipStart()
        print(" ", end="")
        print("##" * (self.width - 2), end="\n\r")
        
    
    def skipStart(self):
        if self.start:
            print(" " * self.start, end="")

# print(self.term.move_xy(self.start, 1))

GameGui2p()