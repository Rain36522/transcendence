from rest_framework import serializers
from .models import Chat, Message
from user.serializers import UserSerializer

class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')
    class Meta:
        model = Message
        fields = '__all__'

