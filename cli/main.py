import sys
import os
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_parent)

# Maintenant, tu peux importer le module depuis le dossier parent
from color import *
from init.initGame import NewGameSettings
from init.user import User
from init.DjangoHttpsCommunication import DjangoCommunication
from init.tools import *
from game.DataTransmission import DataTransmission
from ascii import Ascii
from time import sleep


def getUrl(Django):
    url = inputText("TRANSCENDANCE", "Write the server url.", defaultValue="https://127.0.0.1")
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
    Ascii = Ascii()
    os.system("clear")
    Django = DjangoCommunication()
    # Ascii.putString("TRANSCENDENCE",GREEN, RESET)
    # sleep(4)
    # Information("TRANSCENDANCE", "Welcome to the transcendance CLI")
    getUrl(Django)
    User(Django)
    return Django


async def runCli(Django):
    while True:
        gameSettings = NewGameSettings(Django).gameSettings
        if not gameSettings:
            Information("UNKNOW ERROR", "Unknow Error! Retry!", style=STYLERROR)
        else:
            dataTransmission = DataTransmission(gameSettings["gameId", Django.url])
            

# if __name__ == "__main__":
#     django = "ws://daphne:8002/wsgameserver/"
#     Serveur = WebSocketServer("0.0.0.0", 8001)
#     djangoCli = DjangoCli(Serveur, django)

#     asyncio.get_event_loop().create_task(Serveur.start_server())
#     asyncio.get_event_loop().run_until_complete(djangoCli.connectDjango())
#     print("Django connection completed")
#     asyncio.get_event_loop().create_task(djangoCli.receive_messages())
#     asyncio.get_event_loop().create_task(djangoCli.sendDjangoMsg())
#     asyncio.get_event_loop().run_forever()