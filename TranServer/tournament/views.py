from django.shortcuts import render

def tournament_settings(request):
    return render(request, 'html/tournament.html')
