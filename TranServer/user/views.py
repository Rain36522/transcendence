from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from django.views import generic
from .forms import CustomUserCreationForm, InvitationForm, AcceptInviteForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import (
    UserSerializer,
    SerializerPersonalProfile,
    SerializerOtherProfile,
)
import mimetypes
import os
from django.conf import settings


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def api_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({"message": "User created successfully"}, status=201)
    return Response(serializer.errors, status=400)


@login_required
def invite_user(request):
    current_user = request.user

    invite_form = InvitationForm(current_user)
    accept_form = AcceptInviteForm(current_user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "invite":
            invite_form = InvitationForm(current_user, request.POST)
            if invite_form.is_valid():
                username = invite_form.cleaned_data["username"]
                invited_user = User.objects.get(username=username)
                if invited_user in current_user.invites.all():
                    messages.warning(request, f"User {username} is already invited.")
                else:
                    current_user.invites.add(invited_user)
                    messages.success(request, f"Invitation sent to {username}.")

        elif action == "accept":
            accept_form = AcceptInviteForm(current_user, request.POST)
            if accept_form.is_valid():
                accept_from_user = accept_form.cleaned_data["accept_from"]
                accept_from_user.invites.remove(current_user)
                current_user.invites.remove(accept_from_user)
                current_user.friends.add(accept_from_user)
                messages.success(
                    request,
                    f"You have accepted the invite from {accept_from_user.username}.",
                )

    return render(
        request,
        "invite_user.html",
        {"invite_form": invite_form, "accept_form": accept_form},
    )


@csrf_exempt
@api_view(["POST"])
@renderer_classes([JSONRenderer])
def user_login_api(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("user_dashboard")
    else:
        return JsonResponse({"error": "Invalid username or password"}, status=400)


@api_view(["GET"])
@renderer_classes([JSONRenderer])
@login_required
def user_profile_pic_api(request, username):
    user = get_object_or_404(User, username=username)
    if user.profile_picture:
        path = user.profile_picture.path
        content_type, _ = mimetypes.guess_type(path)
        with open(path, "rb") as f:
            return HttpResponse(f.read(), content_type=content_type)
    default_image_path = os.path.join(settings.MEDIA_ROOT, "default_profile.png")
    with open(default_image_path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")


@api_view(["POST"])
@renderer_classes([JSONRenderer])
@login_required
def upload_profile_pic_api(request):
    if "profile_picture" in request.FILES:
        profile_picture = request.FILES["profile_picture"]

        # Retrieve the user based on your authentication mechanism
        user = request.user  # Or however you authenticate the user in your app

        # Save the profile picture to the user's profile
        user.profile_picture = profile_picture
        user.save()
        return HttpResponse({"message": "Upload successful"}, status=201)
    return HttpResponse({"message": "No file found"}, status=201)


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "html/register.html"


@login_required
def account_information(request):
    return render(request, "html/accountInformation.html")


def logout_view(request):
    logout(request)
    return redirect("user_login")


@login_required
def test_upload(request):
    return render(request, "html/test_upload.html")


@login_required
def user_dashboard(request):
    return render(request, "html/dashboard.html", {"user": request.user})


def user_login(request):
    return render(request, "html/login.html")


def user_register(request):
    return render(request, "html/register.html")


@login_required
def social_management(request):
    return render(request, "html/socialManagement.html")


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"user": request.user})


@login_required
@api_view(["GET"])
@renderer_classes([JSONRenderer])
def user_info_api(request, username=None):
    if username:
        try:
            user = User.objects.get(username=username)
            serializer = SerializerOtherProfile(user)
            return JsonResponse(serializer.data, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    serializer = SerializerPersonalProfile(request.user)
    return JsonResponse(serializer.data, status=200)
