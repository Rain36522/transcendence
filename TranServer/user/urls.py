from django.urls import path
from .views import (
    SignUpView,
    account_information,
    user_dashboard,
    user_login,
    user_register,
    social_management,
    user_login_api,
    api_signup,
    logout_view,
    user_profile_pic_api,
    upload_profile_pic_api,
    test_upload,
    user_info_api,
)
from django.views.generic.base import RedirectView


urlpatterns = [
    path("accountInformation/", account_information, name="account_information"),
    path("dashboard/", user_dashboard, name="user_dashboard"),
    path("login/", user_login, name="user_login"),
    path("register/", user_register, name="user_register"),
    path("socialManagement/", social_management, name="social_management"),
    path("", RedirectView.as_view(url="dashboard/", permanent=True)),
    path("api/login/", user_login_api, name="login_api"),
    path(
        "api/profile_pic/<str:username>/",
        user_profile_pic_api,
        name="user_profile_pic_api",
    ),
    path("api/upload_profile/", upload_profile_pic_api, name="upload_profile_pic_api"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("api/signup/", api_signup, name="api_signup"),
    path("logout/", logout_view, name="user_logout"),
    path("test_upload/", test_upload),
    path("api/user_info/<str:username>/", user_info_api, name="user_info_api_other"),
    path("api/user_info/", user_info_api, name="user_info_api_own"),
]
