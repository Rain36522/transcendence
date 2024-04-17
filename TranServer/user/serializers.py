from rest_framework import serializers
from .models import User
import re


def validate_hex_color(value):
    if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
        raise serializers.ValidationError("Invalid hexadecimal color format")


class ColorUpdateSerializer(serializers.Serializer):
    ball_color = serializers.CharField(
        max_length=7, required=False, validators=[validate_hex_color]
    )
    paddle_color = serializers.CharField(
        max_length=7, required=False, validators=[validate_hex_color]
    )
    enemy_paddle_color = serializers.CharField(
        max_length=7, required=False, validators=[validate_hex_color]
    )
    frame_color = serializers.CharField(
        max_length=7, required=False, validators=[validate_hex_color]
    )
    background_color = serializers.CharField(
        max_length=7, required=False, validators=[validate_hex_color]
    )


class UserSerializer_Username(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "username": {"required": True},
            "email": {"required": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PersonalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "wins",
            "total_games",
        ]


class OtherUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "date_joined", "wins", "total_games"]


class ColorsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "ball_color",
            "paddle_color",
            "enemy_paddle_color",
            "frame_color",
            "background_color",
        ]
