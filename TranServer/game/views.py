from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from .models import Game, GameUser
from rest_framework.views import APIView
from .serializers import GameSettingsSerializer
from asgiref.sync import async_to_sync
import sys
from channels.layers import get_channel_layer
import json
from .consumer import launchGame
from chat.models import Chat, Message
from django.utils import timezone
from django.db.models import Count
from django.http import Http404



def send_message_to_chat_group(chat, message, inviter, user, hostname):
    invite_message = (
        inviter + " has invited you to the game: https://" + hostname + message
    )
    Message.objects.create(
        sender=user,
        chat=chat,
        content=invite_message,
        timestamp=timezone.now(),
    )
    channel_layer = get_channel_layer()
    room_group_name = f"chat_{chat.id}"

    # Send message to group
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            "type": "chat_message",
            "message": invite_message,
            "user": user.username,  # Change this to the desired sender username or identifier
        },
    )


# @login_required
class newGame(APIView):
    def get(self, request):
        return render(request, "html/gameSettings.html")

    def post(self, request):
        data = self.changeData(request.data.copy())
        if data:
            serializer = GameSettingsSerializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()
                # Enregistre les données et récupère l'objet sauvegardé
                self.addPlayer(instance, request.user)
                for game_user in instance.gameuser_set.all():
                    user = game_user.user
                    personal_chat = (
                        Chat.objects.annotate(participant_count=Count("participants"))
                        .filter(
                            is_personal=True, participants=user, participant_count=1
                        )
                        .first()
                    )
                    send_message_to_chat_group(
                        personal_chat,
                        "/game/" + str(instance.id),
                        request.user.username,
                        user,
                        request.META.get("HTTP_HOST", ""),
                    )
                launchGame(instance)
                return JsonResponse(
                    {"gameLink": "/game/" + str(instance.id)}, status=200
                )
            else:
                print("New game,", serializer.errors, file=sys.stderr)
        print("no data for newGame", file=sys.stderr)
        return HttpResponse("Error 400", status=400)

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
            if float(data["acceleration"]):
                data["acceleration"] = float(data["acceleration"]) / 100

            return data
        return None

    def sendNewGame(self, data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gameServer",
            {
                "type": "send_data",
                "data": json.dumps(data),
            },
        )

    def addPlayer(self, game, user):
        game_user = GameUser.objects.create(user=user, game=game)
        game.gameuser_set.add(game_user)


def gamePage(request, id):
    if not isGameFinish(id):
        raise Http404("Game does not exist")
    game = Game.objects.get(pk=id)
    solo = False
    if game.gamemode == 3:
        player = 1
        solo = True
    elif game.gamemode == 0:
        player = 2
        solo = True
    elif game.gamemode == 1:
        player = 2
    else:
        player = 4
    if game.tournament:
        tournamentid = game.tournament.id
    else:
        tournamentid = 0
    contexte = {
        "nbPlayers": player,
        "paddleWidth": 0.02,
        "paddleLength": game.planksize,
        "paddleOffset": 0.02,
        "ballSize": game.ballwidth,
        "isSolo": solo,
        "status": "waiting",
        "user": request.user.username,
        "gameid": id,
        "tournamentid": tournamentid
    }
    contexte_json = json.dumps(contexte)
    return render(request, "monapp/pong.html", {"contexte_json": contexte_json})

def isGameFinish(id):
    if not Game.objects.filter(pk=id).exists():
        return False
    game = Game.objects.get(pk=id)
    if game.gameRunning:
        return True
    gameusers = game.gameuser_set.all()
    for gameuser in gameusers:
        print(gameuser.points)
        if gameuser.points:
            return False
    return True


def home_page(request):
    return render(request, "html/home.html")


