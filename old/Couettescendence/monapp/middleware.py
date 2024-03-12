from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            # Liste des URL pour lesquelles le middleware ne s'appliquera pas
            exceptions = [
                reverse('login'),
                reverse('signup'),
                # Ajoute ici d'autres exceptions au besoin
            ]
            if request.path not in exceptions:
                return redirect(settings.LOGIN_URL)
