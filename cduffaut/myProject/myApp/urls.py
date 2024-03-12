# Dans mon_app/urls.py
from django.urls import path
from . import views  # Assurez-vous d'importer les vues depuis le même répertoire

urlpatterns = [
    path('', views.afficher_message, name='afficher_message'),
]
