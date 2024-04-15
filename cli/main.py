import sys
import os
from color import *
from init.initGame import NewGameSettings
from init.user import User
from init.DjangoHttpsCommunication import DjangoCommunication
from init.tools import *
from game.DataTransmission import DataTransmission
from game.gameGui import GameGui2p
from ascii import Ascii
from time import sleep
import asyncio


def getUrl(Django):
    url = inputText("TRANSCENDANCE", "Write the server url.", defaultValue="https://10.11.13.4")
    if url == None:
        doexit(0, "User exit")
    while not checkUrlInput(url, Django):
        url = inputText("TRANSCENDANCE", "Invalide url. Try again!", style=STYLERROR)
        

def checkUrlInput(url, Django):
    if not url.startswith("https://"):
        return False
    urlSplited = url.split("/")
    if len(url) < 3:
        return False
    url = urlSplited[0] + "//" + urlSplited[2]
    return Django.CheckUrl(url) == 200



def InitCli():
    asciiData = Ascii()
    os.system("clear")
    Django = DjangoCommunication()
    # asciiData.putString("TRANSCENDENCE",GREEN, RESET)
    # sleep(4)
    # Information("TRANSCENDANCE", "Welcome to the transcendance CLI")
    getUrl(Django)
    User(Django)
    return Django

def asWin(message, username):
    if message:
        if message["p1"] > message["p2"] and message["user1"] == username:
            return True, 
        elif message["p1"] < message["p2"] and message["user1"] != username:
            return True
    return False

async def runGame(dataTransmission, gameGui):
    wsKey = asyncio.create_task(dataTransmission.ConnectWsKeyBinding())
    messages_task = asyncio.create_task(dataTransmission.receive_messages())
    game_update_task = asyncio.create_task(gameGui.updateGame())
    return await asyncio.gather(wsKey, messages_task, game_update_task)


if __name__ == "__main__":
    djangocom = InitCli()
    while True:
        gameSettings = NewGameSettings(djangocom).gameSettings
        if not gameSettings:
            Information("UNKNOW ERROR", "Unknow Error! Retry!", style=STYLERROR)
        else:
            dataTransmission = DataTransmission(gameSettings, djangocom.url)
            gameGui = GameGui2p(gameSettings, dataTransmission)
            results = asyncio.run(runGame(dataTransmission, gameGui))
            if str(results[0]).isdigit():
                # os.system("clear")
                Information("ERROR", "Is the game ready to play?", style=STYLERROR)
            elif asWin(results[2], gameSettings["user"]):
                    Information("YOU WIN", "You win this game.", style=STYLSUCCESS)
            else:
                Information("YOU LOOSE", "You loose this game.",style=STYLERROR)
