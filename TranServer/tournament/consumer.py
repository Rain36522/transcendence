from channels.layers import get_channel_layer
import json
from tournament.models import Tournament
from channels.generic.websocket import AsyncWebsocketConsumer


""" Tournament ws manager
When a user join a brodcast of actual state of tournament is send to each player
it s made by the function getUpdate
"""
class TournamentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close()
        self.tournamentId = self.scope['url_route']['kwargs']['tournamentId']
        self.room_group_name = f'tournament_{self.tournamentId}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        data = getUpdate(self.tournamentId)
        await self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # async def receive(self, text_data=None, bytes_data=None):
    #     # Here you should handle incoming messages, but for now, let's just send a response back
    #     print(text_data)




def getUpdate(id):
    tournament = Tournament.objects.get(pk=id)
    data = []
    games = tournament.game_set.all()
    for game in games:
        data.append(putGameInDict(game))
    return data

def putGameInDict(game):
    dico = {}
    gameusers = game.gameuser_set.all()
    i = 0
    dico["gameIs"] = game.id
    for gameuser in gameusers:
        dico['player{}Id'.format(i)] = gameuser.user.username
        dico['score{}'.format(i)] = gameuser.points
        i += 1
    dico["isRuning"] = game.gameRuning
    dico["level"] = game.gameLevel
    dico["pos"] = game.levelPos
    return dico
