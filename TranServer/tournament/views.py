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

import json

class tournament_settings(APIView):
    def get(self, request):
        return render(request, 'html/tournament.html')
    
    def post(self, request):
        self.data = request.data.copy()
        self.tournament = Tournament.objects.create(playerNumber=self.data["playerNumber"])
        self.tournament.players.add(request.user)
        if self.data["gamesettings"] == "0":
            self.generateMixTree(player)
        else:
            self.generateStandardTree(player, game)
        self.createGamesDb()

        return redirect(f'/tournament/id/1')
    

    def getMixLevel(self, player):
        game4p = 1
        game2p = 0
        player -= 4
        while player > 4 and not ((player) / 2) % 2:
            game4p += 1
            player -= 4
        while player >= 8:
            game4p += 1
            player -= 4
        while player:
            game2p += 1
            player -= 2
        if (game2p + game4p) % 2 and game2p >= 2:
            game2p -= 2
            game4p += 1
        elif (game2p + game4p) % 2:
            game4p -= 1
            game2p += 2
        if not game2p and game4p >=  4:
            game2p = 4
            game4p -= 2
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
            listeMatchLevel = getMixLevel(player)
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
    
    def putGamesDb(self, level, model):
        serializer = GameSettingsSerializer(data=data)

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
