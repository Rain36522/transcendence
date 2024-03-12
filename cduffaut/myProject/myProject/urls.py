# Dans mon_projet/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myApp.urls')),  # Assurez-vous d'inclure les URLs de mon_app
]
