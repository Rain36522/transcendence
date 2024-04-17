from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db.models import F
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
from user.models import User
from game.models import Game, GameUser
from game.serializers import GameSettingsSerializer
from game.consumer import launchGame
import json
from random import choice
from .consumer import getUpdate
from game.views import newGame

"""Tournament settings management

This function generate all the game instance in database. with information.
after that, the user is added as player inside tournament.
When it s made, the user is redirected to the page for adding user in tournament
"""
class tournamentSettings(APIView):

    renderer_classes = [JSONRenderer]

    def get(self, request):
        return render(request, 'gamesettingspage.html')
    
    def post(self, request):
        print("REQUEST TOURNAMENT POST", file=sys.stderr)
        self.data = request.data.copy()
        self.tournament = Tournament.objects.create(playerNumber=self.data["playerNumber"])
        print("Tournament DB ID", self.tournament.id)
        self.data["tournament"] = self.tournament.id
        if self.data["gamesettings"] == "0":
            self.GenerateMixTree(int(self.data["playerNumber"]))
        elif self.data["gamesettings"] == "2":
            self.generateStandardTree(int(self.data["playerNumber"]), 2)
        else:
            self.generateStandardTree(int(self.data["playerNumber"]), 4)
        if not self.createGamesDb():
            print("DB not created!")
            return HttpResponse("Error 500", status=500) # TODO rediriger vers error page
        putUserInGame(self.tournament, request.user)
        return redirect('/tournament/' + str(self.tournament.id)) 
        # return render(request, 'addUser.html', {'id': self.tournament.id})


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

    def GenerateMixTree(self, player : int):
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
            
                
    def generateStandardTree(self, player : int, gameplayer : int):
        self.MatchListe = []
        while player >= gameplayer:
            player = player // gameplayer
            self.MatchListe.append([gameplayer] * player)


        # game = Game.objects.create(tournament=tournament)

    def createGamesDb(self):
        i = len(self.MatchListe) - 1
        firstGameDb = True
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
                            print("ELELEMENT :", element, file=sys.stderr)
                            element[0] -= 1
                            break
                id = self.putGamesDb(i, j, gamePlayer, nextGameId, firstGameDb)
                firstGameDb = False
                if not id:
                    return False
                liste.append([gamePlayer, id])
                j += 1
            oldListe = liste.copy()
            i -= 1
        return True
    
    def putGamesDb(self, level, levelPos, gameMode, nextGameId, firstGameGenerated):
        if gameMode == 2:
            self.data["gamemode"] = 1
        else:
            self.data["gamemode"] = 2
        self.data["gameLevel"] = level
        self.data["levelPos"] = levelPos
        if nextGameId:
            self.data["nextGame"] = nextGameId
        if firstGameGenerated:
            self.data = self.changeData(self.data)
        serializer = GameSettingsSerializer(data=self.data)
        if serializer.is_valid():
            return serializer.save().id
        else:
            errors = serializer.errors
            print("ERROR DB : ", errors, file=sys.stderr)
            return None
    
    def changeData(self, data):
        if (
            data.get("ballwidth")
            and data.get("planksize")
            and data.get("Speed")
            and data.get("acceleration")
        ):
            data["ballwidth"] = int(data["ballwidth"]) / 100
            data["planksize"] = int(data["planksize"]) / 100
            data["Speed"] = float(data["Speed"]) / 10
            if int(data["acceleration"]):
                data["acceleration"] = int(data["acceleration"]) / 100

            return data
        return None

    
# def TournamentAddUser(request, id):
#     return render(request, 'addUser.html')

""" Tournament view
When a user join a tournament view:
if the user is in the tournament, and as to play, he is automatically redirected to the game page.
In other case, if the user is not added, he is added to the tournament.

When the last player join, the game instance is launch. and an update is send.
"""
class TournamentView(APIView):

    renderer_classes = [JSONRenderer]

    def get(self, request, id):
        print("USER ACCESS TO TOURNAMENT VIEW")
        self.id = id
        self.request = request
        id = self.newUserConnection()
        # if id:
            # return redirect("/game/" + str(id) + "/")
        tournamentSize = self.getGameByLevel()
        return render(request, 'html/bracket.html', {'tournamentSize': tournamentSize})

    def getGameByLevel(self):
        i = 0
        gameliste = []
        value = 1
        while value:
            value = self.tournament.game_set.filter(gameLevel=i).count()
            if value:
                gameliste.append(value)
            i += 1
        print("RESULT LISTE", gameliste)
        return gameliste


    # if user as to play: return gameid
    def newUserConnection(self):
        self.tournament = Tournament.objects.get(pk=self.id)
        user_ids = self.tournament.game_set.all().values_list('gameuser__user', flat=True)
        usernames = User.objects.filter(id__in=user_ids).values_list('username', flat=True)
        print("CHECKING USERS", usernames)
        if str(self.request.user) in usernames:
            print("USER ALREADY IN GAME")
            return self.checkUserState()
        elif user_ids.count() <= self.tournament.playerNumber:
            print("USER NOT IN GAME")
            if putUserInGame(self.tournament, self.request.user):
                launchTournament(self.tournament)
        else:
            print("USER IS A VISITOR")
        return 0
    
    def checkUserState(self):
        # Filtre les jeux de ce tournoi où gameuser est cette instance et gameRunning est True
        game = self.tournament.game_set.filter(gameRunning=True, gameuser__user=self.request.user)
        print("USER WAITED ON GAME :", game)
        if game:
            return game[0].id

def putUserInGame(tournament, user):
    games = tournament.game_set.filter(gameLevel=0)
    availablGame = []
    availablPlace = 0
    for game in games:
        if game.gamemode == 1 and game.gameuser_set.count() < 2:
            availablGame.append(game)
            availablPlace += 2 - game.gameuser_set.count()
        elif game.gamemode == 2 and game.gameuser_set.count() < 4:
            availablGame.append(game)
            availablPlace += 4 - game.gameuser_set.count()
    if availablGame:
        game = choice(availablGame)
        user = GameUser.objects.create(user=user, game=game)
        game.gameuser_set.add(user)
        tournament.playerNumber = int(tournament.playerNumber) + 1
    if availablPlace == 1:
        return True
    return False


def launchTournament(tournament):
    games = tournament.game_set.filter(gameLevel=0)
    for game in games:
        launchGame(game)
    getUpdate(tournament.id)
