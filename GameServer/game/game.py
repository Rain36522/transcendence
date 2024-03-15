import os
from wsClient import WebSocketClient
from gameLogic import gameLogic
from json import loads
import asyncio
from time import sleep

# Convertir JSON en dictionnaire
# gameSettings = loads(os.environ.get("newGame"))

gameSettings = None
#dictionary communication bitween serveur and client.
game = {
	"ballx" : 0,
	"bally" : 0,
	"p1" : 0,
	"p2" : 0,
	"p3" : 0,
	"p4" : 0,
	"state" : "pause",
	"score1" : 0,
	"score2" : 0,
	"score3" : 0,
	"score4" : 0
}

# Exemple d'utilisation du client WebSocket avec asyncio
if __name__ == "__main__":
    #waiting wsServeur start for auto start test
    sleep(3)
    # Création d'un client WebSocket
    #client = WebSocketClient("ws://localhost:8001/game/" + gameSettings["gameid"])
    client = WebSocketClient("ws://localhost:8001/game/1")

    # Lancement du client WebSocket en parallèle
    asyncio.get_event_loop().run_until_complete(client.connect())
    asyncio.get_event_loop().create_task(client.receive_messages())

    # Lancement de la boucle d'événements asyncio pour attendre la connexion
    # Création d'une tâche pour exécuter une autre fonction en parallèle
    gameLogicInstance = gameLogic(client, gameSettings, game)
    asyncio.get_event_loop().create_task(gameLogicInstance.gameInput())

    # Lancement de la boucle d'événements asyncio
    asyncio.get_event_loop().run_forever()