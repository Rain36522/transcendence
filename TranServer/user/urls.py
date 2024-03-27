from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView
from .views import profile, invite_user
from .views import dashboard
from .views import profil_utilisateur
from .views import account_information, user_dashboard, user_login, user_register, social_management
from django.views.generic.base import RedirectView


urlpatterns = [
    path ('accountInformation/', account_information, name='account_information'),
    path ('dashboard/', user_dashboard, name='user_dashboard'),
    path ('login/', user_login, name='user_login'),
    path ('register/', user_register, name='user_register'),
    path ('socialManagement/', social_management, name='social_management'),

    path('', RedirectView.as_view(url='login', permanent=True)),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('signup/', SignUpView.as_view(), name='signup'),
    # path('profile/', profile, name='profile'),
    # path('profile/dashboard/', dashboard, name='dashboard'),
    # path('profile/<str:username>/', views.profil_utilisateur, name='profile'),
    # path('invite/', invite_user, name='invite'),
]
