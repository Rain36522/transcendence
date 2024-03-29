from color import *
from initGame import NewGameSettings
from user import User
from DjangoHttpsCommunication import DjangoCommunication
from tools import *

def getUrl(Django):
    url = inputText("TRANSCENDANCE", "Write the server url.")
    while url and not checkUrlInput(url, Django):
        url = inputText("TRANSCENDANCE", "Invalide url. Try again!", style=STYLERROR)
    if not url:
        doexit(0)

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
    Information("TRANSCENDANCE", "Welcome to the transcendance CLI")
    getUrl(Django)
    User(Django)
    NewGameSettings()
    Information("FINISH", "FINISH", style=STYLSUCCESS)


if __name__ == '__main__':
    InitCli()