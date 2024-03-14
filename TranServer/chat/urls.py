from django.urls import path
from .views import ChatListView, chat_view, chat_message_view

urlpatterns = [
     path('api/chats/', ChatListView.as_view(), name='chat_list_api'),
     path('api/chats/<str:chat_id>/', chat_message_view, name='chat_message_api'),
     path('chats/', chat_view, name='chats'),
]