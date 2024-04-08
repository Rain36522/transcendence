from channels.layers import get_channel_layer
import json
from channels.generic.websocket import AsyncWebsocketConsumer

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

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # async def receive(self, text_data=None, bytes_data=None):
    #     # Here you should handle incoming messages, but for now, let's just send a response back
    #     print(text_data)

    async def send_data(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))