from django.shortcuts import render

def tournament_settings(request):
    return render(request, 'html/tournament.html')

def bracket(request):
    return render(request, 'html/bracket.html')
