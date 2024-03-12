# Dans mon_app/views.py
from django.http import HttpResponse

def afficher_message(request):
    return HttpResponse("Sono nel club con la mia gang, la tua hoe sta guardando.")
