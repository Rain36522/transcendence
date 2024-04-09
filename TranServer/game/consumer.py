import json
from channels.generic.websocket import AsyncWebsocketConsumer
from tournament.consumer import putGameInDict
from .models import Game, GameUser
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.middleware.csrf import get_token


"""Game ws manager
Manage the connection between game server and django.
Send tournament update in case of tournament game end.
Also set the winer as next game player
"""

class GameServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.path = self.scope['path']
        self.group_name = "gameServer"
        self.channel_layer = get_channel_layer()

        # Ajoute le consommateur WebSocket au groupe
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Implement any necessary cleanup logic here
        await self.channel_layer.group_discard("gameServer", self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Here you should handle incoming messages, but for now, let's just send a response back
        data = json.loads(text_data)
        game = Game.objects.get(pk=data["gameid"])
        winer = await self.putGameResultDb(game, data)
        tournamentId = game.tournament_set.id
        if tournamentId:
            await self.tournamentEndGame(tournamentId, game, winer)
        
    async def tournamentEndGame(self, tournamentId, game, winer):
        if game.nextGame:
            next = game.nextGame_set.id
            newuser = GameUser.objects.create(user=winer.user, game=next)
            game.gameuser_set.add(newuser)
            if game.gameuser_set.count() == game.gamemode * 2:
                launchGame(next)

        self.sendUpdateTournamentview(next, tournamentId)
                
    
    async def putGameResultDb(self, game, data): #return winer
        point = 0
        winer = None 
        game.gameRunning = False
        gameusers = game.gameuser_set.all()
        for gameuser in gameusers:
            for cle, value in data.items():
                if cle.startswith("user") and value[0] == gameuser.user_set.username:
                    gameuser.points = value[1]
                    if point < value[1]:
                        point = value[1]
                        winer = gameuser
                    break
        return winer

    async def sendUpdateTournamentview(self, game, tournamentId):
        async_to_sync(self.channel_layer.group_send)(
            'tournament_' + str(tournamentId),
            {
                'type': 'end_game',
                'message': putGameInDict(game),
            }
            )
        
    async def send_data(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))


"""Launch game instance
This class take the information and send for launching a game instance.
"""
class launchGame:
    def __init__(self, game):
        self.chanelLayer = get_channel_layer()
        data = self.generateGame(game, self.generateDico(game))
        self.sendData(data)
        game.gameRunning = True

    def generateDico(self, game):
        dico = {}
        dico["gameid"] = game.id
        dico["ballwidth"] = game.ballwidth
        dico["planksize"] = game.planksize
        dico["Speed"] = game.Speed
        dico["winpoint"] = game.winpoint
        return dico
    
    def generateGame(self, game, dico):
        if game.gamemode == 0 or game.gamemode == 1: #2p offline, 2p online
            dico["playeramount"] = 2
        elif game.gamemode == 2: # 4p
            dico["playeramount"] = 4
        else: #game.gamemode = 3 = IA
            dico["playeramount"] = 1
        users = game.gameuser_set.all()
        i = 0
        for user in users:
            dico["user{}".format(i)] = get_token(user)
        return dico
    
    def sendData(self, data):
        async_to_sync(self.chanelLayer.group_send)(
            'gameServer',
            {
                'type': 'new_game',
                'message': json.loads(data),
            }
        )
