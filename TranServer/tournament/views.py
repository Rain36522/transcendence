from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
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
from game.models import Game, GameUser
from game.serializers import GameSettingsSerializer
from game.consumer import launchGame
import json
from random import choice
from .consumer import getUpdate

"""Tournament settings management

This function generate all the game instance in database. with information.
after that, the user is added as player inside tournament.
When it s made, the user is redirected to the page for adding user in tournament
"""
class tournamentSettings(APIView):
    def get(self, request):
        return render(request, 'html/tournament.html')
    
    def post(self, request):
        self.data = request.data.copy()
        self.tournament = Tournament.objects.create(playerNumber=self.data["playerNumber"])
        if self.data["gamesettings"] == "0":
            self.generateMixTree(self.data["playerNumber"])
        elif self.data["gamesettings"] == "1":
            self.generateStandardTree(self.data["playerNumber"], 2)
        else:
            self.generateStandardTree(self.data["playerNumber"], 2)
        self.createGamesDb()
        putUserInGame(self.tournament, request.user)
        return render(request, 'addUser.html', {'id': self.tournament.id})


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
        i = len(self.MatchListe) - 1
        oldListe = None
        for level in reversed(self.MatchListe):
            j = 0
            liste = []
            for gamePlayer in level: # iterate game in level. value 2 or 4
                nextGameId = 0
                if oldListe:
                    for element in oldListe:
                        if element[0]:
                            nextGameId = element[1]
                            element[0] -= 1
                            break
                id = self.putGamesDb(i, j, gamePlayer, nextGameId)
                liste.append((gamePlayer, id))
                j += 1
            oldListe = liste.copy()
            i -= 1
    
    def putGamesDb(self, level, levelPos, gameMode, nextGameId):
        if gameMode == 2:
            self.data["gamemode"] = 1
        else:
            self.data["gamemode"] = 2
        self.data["gameLevel"] = level
        self.data["levelPos"] = levelPos
        self.data["nextGame"] = nextGameId
        serializer = GameSettingsSerializer(data=self.data)
        # Vérifier la validité du sérialiseur
        if serializer.is_valid():
            # Sauvegarder les données dans la base de données
            serializer.save()
        return serializer.id
    
# def TournamentAddUser(request, id):
#     return render(request, 'addUser.html')

""" Tournament view
When a user join a tournament view:
if the user is in the tournament, and as to play, he is automatically redirected to the game page.
In other case, if the user is not added, he is added to the tournament.

When the last player join, the game instance is launch. and an update is send.
"""
class TournamentView(APIView):
    def get(self, request, id):
        self.id = id
        self.request = request
        id = self.newUserConnection()
        if id:
            return redirect("/game/" + str(id) + "/")
        # return HttpResponse("Success", "username":request.user.username)

    # if user as to play: return gameid
    def newUserConnection(self):
        self.tournament = Tournament.objects.get(pk=self.id)
        if self.request.user in self.tournament.players:
            return self.checkUserState()
        elif self.tournament.gameuser_set.count() < self.tournament.playerNumber:
            if putUserInGame(self.tournament, self.request.user):
                launchTournament(self.tournament)
        return 0
    
    def checkUserState(self):
        game = self.tournament.game_set.filter(players=self.request.user, gameRuning=True)
        if game:
            return game[0].id

def putUserInGame(tournament, user):
    games = tournament.game_set.filter(gameLevel=0)
    availablGame = []
    availablPlace = 0
    for game in games:
        if game.gamemode == 1 and game.players.count() < 2:
            availablGame.append(game)
            availablPlace += 2 - game.players.count()
        elif game.gamemode == 2 and game.players.count < 4:
            availablGame.append(game)
            availablPlace += 4 - game.players.count()
    if availablGame:
        game = choice(availablGame)
        user = GameUser.objects.create(user=user, game=game)
        game.gameuser_set.add(user)
        tournament.playerNumber += 1
    if availablPlace == 1:
        return True
    return False


def launchTournament(tournament):
    games = tournament.game_set.filter(gameLevel=0)
    for game in games:
        launchGame(game)
    getUpdate(tournament.id)
