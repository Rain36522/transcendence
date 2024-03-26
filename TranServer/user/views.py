from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, InvitationForm, AcceptInviteForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.contrib import messages

@login_required
def invite_user(request):
    current_user = request.user

    invite_form = InvitationForm(current_user)
    accept_form = AcceptInviteForm(current_user)
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'invite':
            invite_form = InvitationForm(current_user, request.POST)
            if invite_form.is_valid():
                username = invite_form.cleaned_data['username']
                invited_user = User.objects.get(username=username)
                if invited_user in current_user.invites.all():
                    messages.warning(request, f'User {username} is already invited.')
                else:
                    current_user.invites.add(invited_user)
                    messages.success(request, f'Invitation sent to {username}.')

        elif action == 'accept':
            accept_form = AcceptInviteForm(current_user, request.POST)
            if accept_form.is_valid():
                accept_from_user = accept_form.cleaned_data['accept_from']
                accept_from_user.invites.remove(current_user)
                current_user.invites.remove(accept_from_user)
                current_user.friends.add(accept_from_user)
                messages.success(request, f'You have accepted the invite from {accept_from_user.username}.')

    return render(request, 'invite_user.html', {'invite_form': invite_form, 'accept_form': accept_form})

# def user_login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')  # Redirige vers la page d'accueil après connexion
#         else:
#             return HttpResponse("Échec de la connexion. Essayez à nouveau.")
#     return render(request, 'login.html')  # Affiche le formulaire de connexion pour une requête GET


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def account_information(request):
    return render(request, 'accountInformation.html')

def user_dashboard(request):
    return render(request, 'dashboard.html')

def user_login(request):
    return render(request, 'login.html')

def user_register(request):
    return render(request, 'register.html')

def social_management(request):
    return render(request, 'socialManagement.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

def profil_utilisateur(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return render(request, 'profil_utilisateur.html', {'user_profil': user})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

def ajouter_resultat(request, points_joueur, points_ennemi, username_ennemi):
    utilisateur = request.user
    nouveau_resultat = [points_joueur, points_ennemi, username_ennemi]
    historique_actuel = utilisateur.historique_resultats
    historique_actuel.append(nouveau_resultat)
    utilisateur.historique_resultats = historique_actuel
    utilisateur.save()

def home(request):
    return HttpResponse('Bienvenue sur la page d\'accueil !')