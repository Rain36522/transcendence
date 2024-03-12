import json
from channels.generic.websocket import AsyncWebsocketConsumer

'''
	Cette classe gère les connexions WebSocket, 
    la réception de messages, et l'envoi de réponses. 
    Vous pouvez adapter le contenu de la méthode receive 
    pour répondre à vos besoins spécifiques.
'''

class MyChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
