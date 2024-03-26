import os
from wsClient import WebSocketClient
from gameLogic import gameLogic
import json
import asyncio
import sys
from time import sleep

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
	"state" : "pause",
	"score1" : 0,
	"score2" : 0,
	"score3" : 0,
	"score4" : 0
}

gameSettings = {
    "ballwidth" : 0.03, #max size plank size calculation
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

def putDatagameSettings(data, settings):
    if data.get("ballwidth"):
        settings["ballwidth"] = data["ballwidth"]
    if data.get("planksize"):
        settings["planksize"] = data["planksize"]
    if data.get("Speed"):
        settings["Speed"] = data["Speed"]
    if data.get("acceleration"):
        settings["acceleration"] = data["acceleration"]
    if data.get("playeramount"):
        settings["playeramount"] = data["playeramount"]
    if data.get("winpoint"):
        settings["winpoint"] = data["winpoint"]
    if data.get("user1"):
        settings["user1"] = data["user1"]
    if data.get("user2"):
        settings["user2"] = data["user2"]
    if data.get("user3"):
        settings["user3"] = data["user3"]
    if data.get("user4"):
        settings["user4"] = data["user4"]
    return settings


# Exemple d'utilisation du client WebSocket avec asyncio
if __name__ == "__main__":
    print("\033[31m", file=sys.stderr)
    #waiting wsServeur start for auto start test
    sleep(3)
    wsServ = "ws://localhost:8001/game/1"
    # Création d'un client WebSocket
    #client = WebSocketClient("ws://localhost:8001/game/" + gameSettings["gameid"])
    client = WebSocketClient(wsServ)
    DjangoData = json.loads(json.loads(os.environ.get("newGame")))
    gameSettings = putDatagameSettings(DjangoData, gameSettings)
    # Lancement du client WebSocket en parallèle
    asyncio.get_event_loop().run_until_complete(client.connect())
    asyncio.get_event_loop().create_task(client.receive_messages())

    # Lancement de la boucle d'événements asyncio pour attendre la connexion
    # Création d'une tâche pour exécuter une autre fonction en parallèle
    gameLogicInstance = gameLogic(client, gameSettings, game)
    asyncio.get_event_loop().create_task(gameLogicInstance.gameInput())

    # Lancement de la boucle d'événements asyncio
    asyncio.get_event_loop().run_forever()