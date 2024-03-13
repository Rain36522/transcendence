
from django.urls import path, include
from .views import newGame

urlpatterns = [
    
    path('newGame/', newGame, name='newGame')
]