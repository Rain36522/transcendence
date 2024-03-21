
from django.urls import path, include
from .views import newGame

urlpatterns = [
    path('newGame/', newGame.as_view(), name='newGame'),
    # path('api/chat/<str:game_id>/', name='newgame_api'),
]