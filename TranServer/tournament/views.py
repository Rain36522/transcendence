from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # Import JSONRenderer
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
import sys
from time import time
import asyncio
from channels.layers import get_channel_layer
from django.shortcuts import redirect
from random import randint
from .models import Tournament
from game.models import Game
from game.serializers import GameSettingsSerializer

import json

class tournament_settings(APIView):
    def get(self, request):
        return render(request, 'html/tournament.html')
    
    def post(self, request):
        self.data = request.data.copy()
        self.tournament = Tournament.objects.create(playerNumber=self.data["playerNumber"])
        self.tournament.players.add(request.user)
        if self.data["gamesettings"] == "0":
            self.generateMixTree(self.data["playerNumber"])
        elif self.data["gamesettings"] == "1":
            self.generateStandardTree(self.data["playerNumber"], 2)
        else:
            self.generateStandardTree(self.data["playerNumber"], 2)
        self.createGamesDb()

        return redirect(f'/tournament/id/1')
    

    def getMixLevel(self, player):
        game2p = 0
        game4p = 0
        while player >= 6:
            player -= 6
            game2p += 1
            game4p += 1
        while player >= 4:
            player -= 4
            game4p += 1
        while player >= 2:
            player -= 2
            game2p += 1
        if (game4p + game2p) % 2 and game4p:
            game4p -= 1
            game2p += 2
        elif (game4p + game2p) % 2:
            game2p -= 2
            game4p += 1
        liste = []
        while game4p and game2p:
            if randint(1, 2) % 2:
                liste.append(4)
                game4p -= 1
            else:
                liste.append(2)
                game2p -= 1
        while game4p:
            liste.append(4)
            game4p -= 1
        while game2p:
            liste.append(2)
            game2p -= 1
        return liste

    def GenerateMixTree(self, player):
        self.MatchListe = []
        while player >= 6:
            listeMatchLevel = self.getMixLevel(player)
            player = len(listeMatchLevel)
            self.MatchListe.append(listeMatchLevel)
        if player == 4:
            liste = [4]
        else:
            liste = [2]
        self.MatchListe.append(liste)
            
                
    def generateStandardTree(self, player, gameplayer):
        self.MatchListe = []
        while player >= gameplayer:
            print("loop")
            player = player // gameplayer
            self.MatchListe.append([gameplayer] * player)


        # game = Game.objects.create(tournament=tournament)

    def createGameDb(self):
        i = 0
        for level in self.MatchListe:
            for gamePlayer in level:
                self.putGamesDb(i, gamePlayer)
            i += 1
    
    def putGamesDb(self, level, gameMode):
        if gameMode == 2:
            self.data["gamemode"] = 1
        else:
            self.data["gamemode"] = 2
        serializer = GameSettingsSerializer(data=self.data)
        # Vérifier la validité du sérialiseur
        if serializer.is_valid():
            # Sauvegarder les données dans la base de données
            serializer.save()


class TournamentView(APIView):
    def get(self, request, id):
        self.id = id
        print("id :", id)
        return HttpResponse("Success")

    def addUser(self):
        tournament = Tournament.objects.get(pk=self.id)
        Tournament.add(request.user)
    def getData(self):
        pass

def sendNewGame(self, dat, id):
    print("sending new msg")
    data = json.dumps(data)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
    "tournament_" + id,
    {
        "type": "send_data",
        "data": data,
    }
    )
    print("message send")
