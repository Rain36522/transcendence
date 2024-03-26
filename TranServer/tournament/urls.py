from django.urls import path
from . import views
#cecile
from django.urls import tournament_settings

#cecile
urlpatterns = [
    path ('tournamentSettings/', tournament_settings, name='tournament_settings'),
]