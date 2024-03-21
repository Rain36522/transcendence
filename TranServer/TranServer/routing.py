from django.urls import re_path
from chat.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/your_url/$', ChatConsumer.as_asgi()),
]