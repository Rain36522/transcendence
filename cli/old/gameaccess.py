from color import *
from os import system
import re

class GameAccess:
    def __init__(self):
        self.wsServ = ""
        self.JoinCreate()

    def JoinCreate(self):
        choice = ""
        while choice != "1" or choice != "2":
            print(BWHITE, "1 :", WHITE, "Would you like to join a game?", RESET)
            print(BWHITE, "2 :", WHITE, "Would you like to create a game?", RESET)
            choice = input("1 - 2 : ")
            if choice != "1" or choice != "2":
                print(ORANGE, "Wrong input!", RESET)
        system("clear")
        if choice == "1":
            self.joinGame()
        elif choice == "2":
            self.createGame()
    
    #change url len and data TODO
    def joinGame(self):
        print(BWHITE, "Joining game", RESET)
        while True:
            url = input("Put an existing game url : ")
            if url.startswith("https://") and len(url) == 5 and url[3] == "game" and url[4].isdigit():
                break
            elif url == "e" or url == "exit":
                self.JoinCreate()
            else:
                print(ORANGE, "Wrong URL. Try again!", RESET)
        self.wsServ = "wss://" + url[2] + "/wsGame/" + url[4]
    
    def createGame(self):
        print(BWHITE, "Cretating a new game.", WHITE)
        print("Game settings.")
        ballWidth = self.getIntSettingRange(5, 30, "Ball width (5 - 30), Default 10 : ")
        planksize = self.getIntSettingRange(10, 40, "Plank size (10 - 40),Defaul 15 : ")
        speed = self.getFloatSettingRange(0.5, 3, "Speed (0.5 - 3), Default 1 : ")
        acceleration = self.getIntSettingRange(0, 10, "Acceleration at each bounce (0 - 10), Default 0 : ")
        winpoint = self.getIntSettingRange(0, 10, "Win point (3 - 15), Default 5 : ")
        playerAmount = self.getSetting(("1", "2", "4"), "Player number (1 - 2 - 4) : ")
        #bool (true start with y / false else)
        if (playerAmount != "1"):
            online = self.getSetting(("y", "yes", "no", "n"), "Is an online game? : ")[0] == "y"
        else:
            online = False

    def getIntSettingRange(self, min, max, str):
        result = min - 1
        while result < min or result > max:
            value = input(str)
            if value.isdigit():
                result = int(value)
            if not value.isdigit():
                print(ORANGE, "The input accept only digit.", RESET)
            elif result < min or result > max:
                print(ORANGE, "The value must be between", min, "and", str(max) + ".", RESET)

    def getSetting(self, values, str):
        while True:
            value = input(str)
            if value in values:
                return value
            else:
                print("Wrong value input!")
            

    def getFloatSettingRange(self, min, max, str):
        result = min - 1
        while result < min or result > max:
            value = input(str)
            if value.isdigit():
                result = int(value)
            if re.match(r'^\d+(\.\d+)?$', value) and value.count('.') == 1:
                print(ORANGE, "The input accept number with or without dot", RESET)
            elif result < min or result > max:
                print(ORANGE, "The value must be between", min, "and", str(max) + ".", RESET)


        