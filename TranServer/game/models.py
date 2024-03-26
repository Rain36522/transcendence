from django.db import models
from user.models import User
from tournament.models import Tournament

class Game(models.Model):
    # players = models.ManyToManyField(User)
    date = models.DateTimeField(auto_now_add=True)
    gameLevel = models.PositiveIntegerField(default=0)
    # tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)
    ballSize = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    raquetSize = models.DecimalField(max_digits=5, decimal_places=2, default=30)
    gameSpeed = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    gameAcceleration = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    winPoint = models.PositiveIntegerField(default=5)
    gameMode = models.PositiveIntegerField(default=0) #0 offline, 1 2p, 2 4p,

class GameUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # game = models.ForeignKey(Game, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)