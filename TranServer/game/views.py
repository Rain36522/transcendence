from django.shortcuts import render, redirect
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
from .consumer import launchGame


# @login_required
class newGame(APIView):
    def get(self, request):
        print("GET", file=sys.stderr)
        return render(request, 'html/gameSettings.html')
    
    def post(self, request):
        print("POST FROM USER !", file=sys.stderr)
        data = self.changeData(request.data.copy())
        if data:
            print("Data")
            serializer = GameSettingsSerializer(data=data)
            if serializer.is_valid():
                print("Seriallizer")
                instance = serializer.save()  # Enregistre les données et récupère l'objet sauvegardé
                self.addPlayer(instance, request.user)
                launchGame(instance)
                return JsonResponse({"gameLink": "/game/" + str(instance.id)}, status=200)
            else:
                print(serializer.errors)
            print("no data")
        return HttpResponse("Error 400", status=400)
    
    def changeData(self, data):        
        if data.get("ballwidth") and data.get("planksize") and data.get("Speed") and data.get("acceleration"):
            data["ballwidth"] = int(data["ballwidth"]) / 100
            data["planksize"] = int(data["planksize"]) / 100
            data["Speed"] = float(data["Speed"]) / 10
            if int(data["acceleration"]):
                data["acceleration"] = int(data["acceleration"]) / 100

            return data
        return None

    def sendNewGame(self, data):
        print("sending new msg")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        "gameServer",
        {
            "type": "send_data",
            "data": json.dumps(data),
        }
        )
        print("message send")

    def addPlayer(self, game, user):
        print(user)
        game_user = GameUser.objects.create(user=user, game=game)
        game.gameuser_set.add(game_user)

def gamePage(request, id):
    game = Game.objects.get(pk=id)
    solo = False
    if game.gamemode == 3:
        player = 1
        solo = True
    elif game.gamemode == 0:
        player = 1
        solo = True
    elif game.gamemode == 1:
        player = 2
    else:
        player = 4
    contexte = {
        "nbPlayers": player,
        "paddleWidth": 0.02,
        "paddleLength": game.planksize,
        "paddleOffset": 0.02,
        "ballSize": game.ballwidth,
        "isSolo": solo,
        "status": "waiting",
        "user": request.user.username,
        "gameid": id
    }
    print("USER : ", contexte["user"])
    print("gameid : ", contexte["gameid"])
    contexte_json = json.dumps(contexte)
    return render(request, 'monapp/pong.html', {'contexte_json': contexte_json})

def home_page(request):
    return render(request, 'html/home.html')

def online_game(request):
    return render(request, 'html/onlineGame.html')

