import sys
import os
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_parent)

# Maintenant, tu peux importer le module depuis le dossier parent
from color import *
from initGame import NewGameSettings
from user import User
from DjangoHttpsCommunication import DjangoCommunication
from tools import *
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
    Django = DjangoCommunication()

    # Information("TRANSCENDANCE", "Welcome to the transcendance CLI")
    getUrl(Django)
    User(Django)
    NewGameSettings()
    Information("FINISH", "FINISH", style=STYLSUCCESS)


if __name__ == '__main__':
    Ascii = Ascii()
    os.system("clear")
    # Ascii.putString("TRANSCENDENCE",GREEN, RESET)
    # sleep(4)
    InitCli()