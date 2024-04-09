
from django.urls import path, include
from .views import newGame
from .views import home_page, online_game

urlpatterns = [
    path('home/', home_page, name='home_page'),
    path('onlineGame/', online_game, name='online_game'),
    path('newGame/', newGame.as_view(), name='newGame'),
    # path('game/<int:id>/', gamePage, name="gamePage")
]
