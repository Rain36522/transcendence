from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def newGame(request):
    return render(request, 'newGame.html')

# def cecile
def home_page(request):
    return render(request, 'home.html')
def online_game(request):
    return render(request, 'onlineGame.html')
#