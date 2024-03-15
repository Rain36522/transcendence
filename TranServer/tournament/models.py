from django.db import models
from user.models import User

class Tournament(models.Model):
    players = models.ManyToManyField(User, symmetrical=False, related_name='tournaments')