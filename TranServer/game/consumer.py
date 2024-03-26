from channels.layers import get_channel_layer
import json
from channels.generic.websocket import AsyncWebsocketConsumer

channel_layer = get_channel_layer()

class GameServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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
        print(text_data)
        await self.send(text_data="recieved")

    async def send_data(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps(data))