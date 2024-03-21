from django.db import models
from user.models import User
from tournament.models import Tournament

class Game(models.Model):
    players = models.ManyToManyField(User)
    date = models.DateTimeField(auto_now_add=True)
    gameLevel = models.PositiveIntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)
    ballSize = models.DecimalField(max_digits=5, decimal_places=2, default=0.1)
    raquetSize = models.DecimalField(max_digits=5, decimal_places=2, default=0.3)
    gameSpeed = models.DecimalField(max_digits=5, decimal_places=2, default=0.01)
    gameAcceleration = models.DecimalField(max_digits=5, decimal_places=2, default=0.0001)
    winPoint = models.PositiveIntegerField(default=5)
    gameMode = models.PositiveIntegerField(default=0)

class GameUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)