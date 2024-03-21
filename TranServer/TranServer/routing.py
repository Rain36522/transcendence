from django.urls import re_path
from chat.consumer import ChatConsumer
from game.consumer import GameServerConsumer

websocket_urlpatterns = [
    re_path(r'ws/your_url/$', ChatConsumer.as_asgi()),
    re_path(r'wsgameserver/$', GameServerConsumer.as_asgi())
]