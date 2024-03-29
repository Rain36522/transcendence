
from django.urls import path, include
from .views import tournament_settings
from django.urls import path
from . import views

urlpatterns = [
        path ('tournamentSettings/', tournament_settings, name='tournament_settings')
]