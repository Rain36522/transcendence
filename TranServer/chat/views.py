from django.shortcuts import render

from django.http import JsonResponse
from .models import Chat, Message

def chat_list_view(request):
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
            raise Exception("Invalid Access")
        messages = Message.objects.filter(chat=chat)
        data = [{'sender': message.sender.username, 'content': message.content, 'timestamp': message.timestamp} for message in messages]
        return JsonResponse({'messages': data})
    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Chat not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)