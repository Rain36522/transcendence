from django.db import models
from user.models import User
from tournament.models import Tournament

class Game(models.Model):
    players = models.ManyToManyField(User)
    date = models.DateTimeField()
    gameLevel = models.PositiveIntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)


class GameUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)