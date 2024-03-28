from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView
from .views import profile, dashboard, profil_utilisateur, pong_game, home


urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='monapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),
    path('profile/dashboard/', dashboard, name='dashboard'),
    path('profile/<str:username>/', profil_utilisateur, name='profile'),
    path('pong/', pong_game)
]
