from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView
from .views import profile
from .views import dashboard
from .views import profil_utilisateur
from .views import pong_game
from .views import wsstest
from django.urls import path
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='monapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),
    path('profile/dashboard/', dashboard, name='dashboard'),
    path('profile/<str:username>/', views.profil_utilisateur, name='profile'),
    path('pong/', views.pong_game),
    path('wsstest/', views.wsstest),
    path('favicon.ico', RedirectView.as_view(url='https://i1.sndcdn.com/avatars-000894638827-qr5jsd-t240x240.jpg'), name='favicon'),
]
