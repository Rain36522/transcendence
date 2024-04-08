
from django.urls import path, include
from .views import tournament_settings
from .views import bracket
from django.urls import path
from . import views

urlpatterns = [
        path ('tournamentSettings/', tournament_settings, name='tournament_settings'),
        path ('bracket/', bracket, name='bracket'),
]