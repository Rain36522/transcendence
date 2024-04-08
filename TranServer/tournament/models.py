from django.db import models
from user.models import User
# from game.models import Game

class Tournament(models.Model):
    players = models.ManyToManyField(User, symmetrical=False, related_name='tournaments')
    playerNumber = models.PositiveIntegerField()