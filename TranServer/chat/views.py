from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Chat, Message
from .serializers import ChatSerializer
from rest_framework.response import Response


class ChatListView(APIView):
    """Contains the endpoint for getting all of a users' chats,\n
    or getting/creating/deleting a specific chat

    Methods:
        GET (All, One)\n
        POST (One)\n
        DELETE (One)
    """
    def get(self, request, chat_id=None):
        """For a user that is logged in return json containg the chats' id and participants

        Args:
            route (get all chats): /api/chat
            route (one): /api/chat/{chat_id}

        Returns:
            [multiple]
            id: the chat id
            participants: the chat's participants' usernames
        """
        if chat_id is not None:
            # Retrieve a specific chat
            chat = Chat.objects.get(pk=chat_id)
            serializer = ChatSerializer(chat)
            return Response(serializer.data)
        current_user = request.user
        chats = current_user.chats.all()
        data = [{'id': chat.id, 'participants': [participant.username for participant in chat.participants.all()]} for chat in chats]
        return JsonResponse({'chats': data})


def chat_view(request):
    return render(request, 'chat_page.html')

def chat_message_view(request, chat_id):
    try:
        chat = Chat.objects.get(pk=chat_id)
        if not chat.participants.contains(request.user):
           return JsonResponse({'error': 'Insufficient permissions: Access Denied'}, status=401)
        messages = Message.objects.filter(chat=chat)
        data = [{'sender': message.sender.username, 'content': message.content, 'timestamp': message.timestamp} for message in messages]
        return JsonResponse({'messages': data})
    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Chat not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)