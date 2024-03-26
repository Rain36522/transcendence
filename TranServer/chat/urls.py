from django.urls import path
from .views import ChatListView, chat_view, MessageListView, ws_view
from .consumer import ChatConsumer

urlpatterns = [
     path('chats/', chat_view, name='chats'),
     path('api/chat/', ChatListView.as_view(), name='chat_api'),
     path('api/chat/<str:chat_id>/', ChatListView.as_view(), name='chat_api'),
     path('api/messages/<str:chat_id>/', MessageListView.as_view(), name='chat_message_view'),
     path('test/', ws_view, name='ws_view')
]

websocket_urlpatterns = [
    path('ws/your_url/', ChatConsumer.as_asgi()),
]