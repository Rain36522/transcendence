from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(default=timezone.now)
    wins = models.PositiveIntegerField(default=0, verbose_name="Number of wins")
    total_games = models.PositiveIntegerField(
        default=0, verbose_name="Total number of games"
    )
    friends = models.ManyToManyField("self", symmetrical=True)
    blocked = models.ManyToManyField(
        "self", symmetrical=False, related_name="blocked_by"
    )
    invites = models.ManyToManyField(
        "self", symmetrical=False, related_name="sent_invites"
    )
    profile_picture = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )
    objects = CustomUserManager()
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
