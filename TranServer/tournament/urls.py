from django.urls import path
from . import views
from django.urls import tournament_settings

urlpatterns = [
    path ('tournamentSettings/', tournament_settings, name='tournament_settings'),
]