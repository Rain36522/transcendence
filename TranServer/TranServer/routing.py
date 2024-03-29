from django.urls import re_path, path
from chat.consumer import ChatConsumer
from game.consumer import GameServerConsumer

websocket_urlpatterns = [
    path('ws/your_url/<int:chat_id>/', ChatConsumer.as_asgi()),
    re_path(r'ws/your_url/$', ChatConsumer.as_asgi()),
    re_path(r'wsgameserver/$', GameServerConsumer.as_asgi())
]