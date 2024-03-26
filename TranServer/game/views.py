from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # Import JSONRenderer
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from .models import Game, GameUser
from rest_framework.views import APIView
from .serializers import GameSettingsSerializer
import sys
from time import time

# @login_required
class newGame(APIView):
    def get(self, request):
        print("GET", file=sys.stderr)
        return render(request, 'gamesettinspage.html')
    
    def post(self, request):
        print("POST", file=sys.stderr)
        data = self.changeData(request.data)
        if data:
            serializer = GameSettingsSerializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()  # Enregistre les données et récupère l'objet sauvegardé
                game_id = instance.id  # Obtient l'ID de l'objet sauvegardé
                return HttpResponse("Success")
        return HttpResponse("Failure")
    
    def changeData(self, data):
        if data.get("ballSize") and data.get("raquetSize") and data.get("gameSpeed") and data.get("gameAcceleration"):
            pass