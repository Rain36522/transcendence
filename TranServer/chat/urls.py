from django.urls import path
from .views import chat_list_view, chat_view, chat_message_view

urlpatterns = [
	path('api/chats/', chat_list_view, name='chat_list_api'),
     path('api/chats/<str:chat_id>/', chat_message_view, name='chat_message_api'),
     path('chats/', chat_view, name='chats'),
]