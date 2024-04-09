import json
from channels.generic.websocket import AsyncWebsocketConsumer
from tournament.consumer import putGameInDict
from .models import Game, GameUser
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
        gameusers = game.gameuser_set.all()
        for gameuser in gameusers:
            for cle, value in data.items():
                if cle.startswith("user") and value[0] == gameuser.user_set.username:
                    gameuser.points = value[1]
                    break
                
        tournamentId = game.tournament_set.id
            
        if tournamentId:
            async_to_sync(self.channel_layer.group_send)(
                'tournament_' + str(tournamentId),
                {
                    'type': 'fin_de_partie_message',
                    'message': putGameInDict(game),
                }
            )
        
        

    async def send_data(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))

    async def sendTournamentUpdate(self, data):
        pass