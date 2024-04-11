from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige vers la page d'accueil après connexion
        else:
            return HttpResponse("Échec de la connexion. Essayez à nouveau.")
    return render(request, 'monapp/login.html')  # Affiche le formulaire de connexion pour une requête GET


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'monapp/signup.html'


@login_required
def profile(request):
    return render(request, 'monapp/profile.html')


def profil_utilisateur(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return render(request, 'monapp/profil_utilisateur.html', {'user_profil': user})

@login_required
def dashboard(request):
    return render(request, 'monapp/dashboard.html', {'user': request.user})

def ajouter_resultat(request, points_joueur, points_ennemi, username_ennemi):
    # Trouver l'utilisateur et l'ennemi (assure-toi que 'ennemi' existe aussi dans ta base de données)
    utilisateur = request.user
    # Exemple d'ajout d'un résultat dans l'historique
    nouveau_resultat = [points_joueur, points_ennemi, username_ennemi]
    historique_actuel = utilisateur.historique_resultats
    historique_actuel.append(nouveau_resultat)
    utilisateur.historique_resultats = historique_actuel
    utilisateur.save()


import json  # Importez le module json

def pong_game(request):
    #besoin aussi de savoir playerID pour connaitre quel joueur on est
    #besoin de gameID pour faire la connection et potentiellement l'addresse du serveur aussi
    contexte = {
        "nbPlayers": 2,
        "player1Name": "Shrek 1",
        "player2Name": "Fionna 2",
        "player3Name": "Donkey 3",
        "player4Name": "Dragon 4",
        "paddleColor": "white",
        "paddleWidth": 0.02,
        "paddleLength": 0.2,
        "paddleOffset": 0.02,
        "ballSize": 0.05,
        "isSolo": True,
        "isImage": False,
        "status": "playing"
    }

    contexte_json = json.dumps(contexte)
    return render(request, 'monapp/pong.html', {'contexte_json': contexte_json})


def wsstest(request):
    return render(request, 'monapp/wsstest.html')


def home(request):
    return HttpResponse('Bienvenue sur la page d\'accueil !')
