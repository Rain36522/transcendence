from django.shortcuts import render

def tournament_settings(request):
    return render(request, 'tournament.html')
