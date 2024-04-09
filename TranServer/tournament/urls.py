from django.urls import path, include
from .views import tournamentSettings, TournamentView #, TournamentAddUser
from django.urls import path
from . import views

urlpatterns = [
        # path ('tournamentSettings/', tournament_settings, name='tournament_settings'),
        # path ('bracket/', bracket, name='bracket'),
        path ('tournamentSettings/', tournamentSettings.as_view(), name='tournamentSettings'),
        path('tournament/<int:id>/', TournamentView.as_view(), name='TournamentView'),
        # path('tournament/adduser/<int:id>/', TournamentAddUser, name='TournamentAddUser'),
]