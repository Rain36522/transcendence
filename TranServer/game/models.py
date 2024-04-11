from django.db import models
from user.models import User
from tournament.models import Tournament

class Game(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)
    ballwidth = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    planksize = models.DecimalField(max_digits=5, decimal_places=2, default=30)
    Speed = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    acceleration = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    winpoint = models.PositiveIntegerField(default=5)
    gamemode = models.PositiveIntegerField(default=0) #0 offline, 1 2p, 2 4p, 3 IA
    nextGame = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    gameRunning = models.BooleanField(default=False)
    gameLevel = models.PositiveIntegerField(default=0) # level in tournament tree view
    levelPos = models.PositiveIntegerField(default=0) # position in level

class GameUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, default=None)
    points = models.IntegerField(default=0)