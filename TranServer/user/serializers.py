from rest_framework import serializers
from .models import User

class UserSerializer_Username(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'username': {'required': True},
            'email': {'required': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class SerializerPersonalProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'date_joined', 'is_active', 'wins', 'total_games']

class SerializerOtherProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'date_joined', 'is_active', 'wins', 'total_games']
        
class FriendSerializer(serializers.ModelSerializer):
    friends = UserSerializer_Username(many=True)
    class Meta:
        model = User
        fields = ['friends']

class BlockedSerializer(serializers.ModelSerializer):
    friends = UserSerializer_Username(many=True)
    class Meta:
        model = User
        fields = ['friends']