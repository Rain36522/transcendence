from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # Import JSONRenderer
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from .models import Game, GameUser
from rest_framework.views import APIView
from .serializers import GameSettingsSerializer
from asgiref.sync import async_to_sync
import sys
from time import time
import asyncio
from channels.layers import get_channel_layer
import json

# @login_required
class newGame(APIView):
    def get(self, request):
        print("GET", file=sys.stderr)
        return render(request, 'gamesettinspage.html')
    
    def post(self, request):
        print("POST", file=sys.stderr)
        data = self.changeData(request.data.copy())
        if data:
            serializer = GameSettingsSerializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()  # Enregistre les données et récupère l'objet sauvegardé
                data["gameid"] = instance.id  # Obtient l'ID de l'objet sauvegardé
                self.sendNewGame(data)
                return HttpResponse("Success")
        return HttpResponse("Failure")
    
    def changeData(self, data):
        if data.get("ballSize") and data.get("raquetSize") and data.get("gameSpeed") and data.get("gameAcceleration"):
            data["ballSize"] = int(data["ballSize"]) / 100
            data["raquetSize"] = int(data["raquetSize"]) / 100
            if int(data["gameAcceleration"]):
                data["gameAcceleration"] = int(data["gameAcceleration"]) / 100
            return data
        return None

def home_page(request):
    return render(request, 'html/home.html')

def online_game(request):
    return render(request, 'html/onlineGame.html')

def sendNewGame(self, data):
    print("sending new msg")
    data = json.dumps(data)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
    "gameServer",
    {
        "type": "send_data",
        "data": data,
    }
    )
    print("message send")
