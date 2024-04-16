import os
from wsClient import WebSocketClient
from gameLogic import gameLogic
import json
import asyncio
from sys import stderr
from time import sleep
from sys import stderr

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
ORANGE = "\033[38;2;255;165;0m"

# Convertir JSON en dictionnaire
# gameSettings = loads(os.environ.get("newGame"))

#dictionary communication bitween serveur and client.
game = {
	"ballx" : 0, # -0.5 -> 0.5
	"bally" : 0, # -0.5 -> 0.5
	"p1" : 0, # -0.5 -> 0.5
	"p2" : 0, # -0.5 -> 0.5
	"p3" : 0, # -0.5 -> 0.5
	"p4" : 0, # -0.5 -> 0.5
	"state" : "playing",
	"score1" : 0,
	"score2" : 0,
	"score3" : 0,
	"score4" : 0
}

gameSettings = {
    "ballwidth" : 0.03, #max size plank size calculation
    "planksize" : 0.3, #max size 50%
    "Speed" : 0.002,
    "acceleration" : 0.01, #increase speed each bounce
    "playeramount" : 2,
    "winpoint" : 10,
    "user1" : "",
    "user2" : "",
    "user3" : "",
    "user4" : "",
    "gameid" : 0,
}

gameEndDjango = {
    "user1" : ("", 3),
    "user2" : ("", 4),
    "user3" : ("", 5),
    "user4" : ("", 2),
    "gameid" : 0
    }


def listUser(data):
    liste = []
    for cle, value in data.items():
        if cle.startswith("user"):
            if value:
                liste.append(value)
    return liste

async def WaitUntilPlayers(ws, data):
    userlist = listUser(data)
    liste = []
    i = 0
    while len(liste) < data["playeramount"]:
        msgs = ws.getMsg()
        if msgs:
            for msg in msgs:
                if msg.endswith("login"):
                    msg = msg[:-5]
                    print(MAGENTA, "New user connected to game instance", RESET, msg, file=stderr)
                    if userlist:
                        playerFree = data["playeramount"] - len(userlist)
                    else:
                        playerFree = data["playeramount"]
                    print(MAGENTA, "PlayerFree :", playerFree, RESET, file=stderr)
                    if userlist and msg in userlist:
                        print(MAGENTA, "User add in liste know", RESET, file=stderr)
                        liste.append(msg)
                        i += 1
                    elif liste and len(liste) <= playerFree and msg not in liste:
                        print(MAGENTA, "User add in liste", RESET, file=stderr)
                        liste.append(msg)
                    elif not liste and playerFree:
                        print(MAGENTA, "User add in liste", RESET, file=stderr)
                        liste.append(msg)
                elif msg.endswith("logout"):
                    msg = msg[:-6]
                    if msg in liste:
                        print(YELLOW, msg, "disconnected", RESET, file=stderr)
                        liste.remove(msg)
                        if msg in userlist:
                            i -= 1

        await asyncio.sleep(0.1)
    await asyncio.sleep(1)
    await ws.sendUserJoin(liste)
    return liste

def updateUser(userliste, data):
    if data["gamemode"] == 0:
        return ["Player1", "Player2"]
    elif data["gamemode"] == 3:
        userliste.append("IA")
    return userliste


def putDatagameSettings(data, settings):
    elem = ["ballwidth", "planksize", "Speed", "acceleration", "playeramount", "winpoint", "user1", "user2", "user3", "user4", "gameid"]
    if not data.get("gameid"):
        print("\033[31mGameid not available.\033[0m", file=stderr)
        exit(1)
    for i in elem:
        if data.get(i):
            settings[i] = data[i]
    return settings

# # Exemple d'utilisation du client WebSocket avec asyncio
# if __name__ == "__main__":
#     DjangoData = json.loads(os.environ.get("newGame"))["message"]
#     print("Django data : ", DjangoData)
#     gameSettings = putDatagameSettings(DjangoData, gameSettings)
#     #connection with websocket server
#     wsServ = "ws://localhost:8001/game/" + str(gameSettings["gameid"])
#     client = WebSocketClient(wsServ)
#     # Lancement du client WebSocket en parallèle
#     asyncio.get_event_loop().run_until_complete(client.connect())
#     asyncio.get_event_loop().create_task(client.receive_messages())
#     print(MAGENTA, "RECIEVED USER", RESET, file=stderr)
#     userliste = asyncio.get_event_loop().run_until_complete(WaitUntilPlayers(client, DjangoData))
#     userliste = updateUser(userliste, DjangoData)
#     gameLogicInstance = gameLogic(client, gameSettings, game, userliste)
#     asyncio.get_event_loop().create_task(gameLogicInstance.start_game())

#     # Lancement de la boucle d'événements asyncio
#     asyncio.get_event_loop().run_forever()

async def main():
    gameSettings = {
        "ballwidth" : 0.03, #max size plank size calculation
        "planksize" : 0.3, #max size 50%
        "Speed" : 0.002,
        "acceleration" : 0.01, #increase speed each bounce
        "playeramount" : 2,
        "winpoint" : 10,
        "user1" : "",
        "user2" : "",
        "user3" : "",
        "user4" : "",
        "gameid" : 0,
    }

    game = {
        "ballx" : 0, # -0.5 -> 0.5
        "bally" : 0, # -0.5 -> 0.5
        "p1" : 0, # -0.5 -> 0.5
        "p2" : 0, # -0.5 -> 0.5
        "p3" : 0, # -0.5 -> 0.5
        "p4" : 0, # -0.5 -> 0.5
        "state" : "playing",
        "score1" : 0,
        "score2" : 0,
        "score3" : 0,
        "score4" : 0
    }

    print("|[---Creating game instance...---]|")
    DjangoData = json.loads(os.environ.get("newGame"))["message"]
    print("Django data : ", DjangoData)
    gameSettings = putDatagameSettings(DjangoData, gameSettings)
    wsServ = "ws://localhost:8001/game/" + str(gameSettings["gameid"])

    client = WebSocketClient(wsServ)
    await client.connect()
    asyncio.create_task(client.receive_messages())
    print(MAGENTA, "RECIEVED USER", RESET, file=stderr)

    userliste = await WaitUntilPlayers(client, DjangoData)
    userliste = updateUser(userliste, DjangoData)

    print("|[---Userlist---]|", userliste)
    print("|[--Launching game logic instance--]|")
    game_logic_instance = gameLogic(client, gameSettings, game, userliste)
    await game_logic_instance.start_game()  # Assurez-vous que la méthode start est bien définie pour démarrer BottiBotto et toute autre initialisation asynchrone

    print("|[---Game instance created---]|")

if __name__ == "__main__":
    asyncio.run(main())