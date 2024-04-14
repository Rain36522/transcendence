from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.conf import settings
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError


from .models import User
from chat.models import Chat
from .serializers import UserSerializer, UserSerializer_Username
from .forms import CustomUserCreationForm

import mimetypes
import os


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def api_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        chat = Chat.objects.create()
        chat.participants.add(user)
        chat.is_personal = True
        chat.save()
        login(request, user)
        return Response({"message": "User created successfully"}, status=201)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@renderer_classes([JSONRenderer])
@login_required
def api_pending_invite(request):
    try:
        invites = request.user.sent_invites.all()
        return Response(
            UserSerializer_Username(invites, many=True).data,
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FriendListView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request, username=None):
        try:
            friends = request.user.friends.all()
            return Response(
                UserSerializer_Username(friends, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, username=None):
        if not username:
            return Response(
                "Please provide a username", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username)
            if user.friends.filter(username=request.username):
                user.friends.remove(user)
                return Response("Removed user", status=status.HTTP_200_OK)
            return Response("User is not friend", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(
                "User with provided username does not exist",
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class InviteListView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request, username=None):
        try:
            invites = request.user.invites.all()
            return Response(
                UserSerializer_Username(invites, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, username=None):
        if not username:
            return Response(
                "Please provide a username", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username)
            if user.invites.filter(username=username):
                return Response(
                    "Invite already exists", status=status.HTTP_400_BAD_REQUEST
                )
            user.invites.add(user)
            return Response("Added invite", status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username=None):
        if not username:
            return Response(
                "Please provide a username", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username)
            if user.invites.filter(username=request.username):
                user.invites.remove(user)
                return Response("Removed user", status=status.HTTP_200_OK)
            return Response("Invite does not exist", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(
                "User with provided username does not exist",
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BlockedListView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request, username=None):
        try:
            blocked = request.user.blocked.all()
            return Response(
                UserSerializer_Username(blocked, many=True).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, username=None):
        if not username:
            return Response(
                "Please provide a username", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username)
            if user.blocked.filter(username=username):
                return Response("Already blocked", status=status.HTTP_400_BAD_REQUEST)
            user.blocked.add(user)
            return Response("Added blocked", status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username=None):
        if not username:
            return Response(
                "Please provide a username", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username)
            if user.blocked.filter(username=request.username):
                user.blocked.remove(user)
                return Response("Unblocked user", status=status.HTTP_200_OK)
            return Response("User is not blocked", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(
                "User with provided username does not exist",
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def user_login_api(request):
    try:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("user_dashboard")
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)
    except:
        return JsonResponse({"error": "Invalid request"}, status=400)


@api_view(["GET"])
@renderer_classes([JSONRenderer])
@login_required
def user_profile_pic_api(request, username):
    user = get_object_or_404(User, username=username)
    try:
        if user.profile_picture:
            path = user.profile_picture.path
            content_type, _ = mimetypes.guess_type(path)
            with open(path, "rb") as f:
                return HttpResponse(f.read(), content_type=content_type)
        default_image_path = os.path.join(settings.MEDIA_ROOT, "default_profile.png")
        with open(default_image_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except Exception as e:
        return JsonResponse({"error": e}, status=500)


ALLOWED_FILE_TYPES = ["image/jpeg", "image/png"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@api_view(["POST"])
@renderer_classes([JSONRenderer])
@login_required
def upload_profile_pic_api(request):
    try:
        if "profile_picture" in request.FILES:
            profile_picture = request.FILES["profile_picture"]

            # File type validation
            if profile_picture.content_type not in ALLOWED_FILE_TYPES:
                return JsonResponse({"error": "Invalid file type"}, status=400)

            # File size limit
            if profile_picture.size > MAX_FILE_SIZE:
                return JsonResponse(
                    {"error": "File size exceeds the limit"}, status=400
                )

            user = request.user

            # Check if the user already has a profile picture
            if user.profile_picture:
                try:
                    # Delete the old profile picture file from the storage
                    if os.path.isfile(user.profile_picture.path):
                        os.remove(user.profile_picture.path)
                except:
                    pass

            # Save the new profile picture
            user.profile_picture = profile_picture
            user.save()
            return HttpResponse(
                {"message": "Upload successful"}, status=status.HTTP_201_CREATED
            )
        return HttpResponse(
            {"message": "No file found"}, status=status.HTTP_400_BAD_REQUEST
        )
    except ValidationError:
        return JsonResponse(
            {"error": "Invalid file"}, status=status.HTTP_400_BAD_REQUEST
        )
    except:
        return JsonResponse(
            {"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST
        )


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
