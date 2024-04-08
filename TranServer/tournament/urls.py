
from django.urls import path, include
from .views import tournament_settings, TournamentView
from django.urls import path
from . import views

urlpatterns = [
        path ('tournamentSettings/', tournament_settings.as_view(), name='tournament_settings'),
        path('tournament/id/<int:id>/', TournamentView.as_view(), name='TournamentView'),
]