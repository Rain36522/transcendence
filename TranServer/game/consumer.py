from channels.layers import get_channel_layer
import json
from channels.generic.websocket import AsyncWebsocketConsumer

channel_layer = get_channel_layer()

class GameServerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
                    'message': "asdf"
                }))
    async def disconnect(self, close_code):
        # Implement any necessary cleanup logic here
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # Here you should handle incoming messages, but for now, let's just send a response back
        # pass
        if text_data:
            await self.send(text_data=json.dumps({
                    'message': "asdf"
                }))
        elif bytes_data:
            await self.send(bytes_data=bytes_data)