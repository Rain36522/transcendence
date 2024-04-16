from django.urls import path
from .views import (
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
    InviteListView,
    api_pending_invite,
    FriendListView,
    BlockedListView,
    search_usernames_api,
    profile_info_api,
    is_active_api,
    change_password_api,
    test_password_change_view,
    undo_invite_api,
    user_exist_api,
    is_blocked_api,
    profile_user,
    ColorView,
)
from django.views.generic.base import RedirectView


urlpatterns = [
    path("profile_user/", profile_user, name="profile_user"),
    path("accountInformation/", account_information, name="account_information"),
    path("dashboard/", user_dashboard, name="user_dashboard"),
    path("dashboard/<str:username>/", user_dashboard, name="user_dashboard_other"),
    path("login/", user_login, name="user_login"),
    path("register/", user_register, name="user_register"),
    path("socialManagement/", social_management, name="social_management"),
    path("", RedirectView.as_view(url="dashboard/", permanent=True)),
    path("api/login/", user_login_api, name="login_api"),
    path(
        "api/profile_pic/<str:username>/",
        user_profile_pic_api,
        name="user_profile_pic_api_other",
    ),
    path(
        "api/profile_pic/",
        user_profile_pic_api,
        name="user_profile_pic_api",
    ),
    path("api/upload_profile/", upload_profile_pic_api, name="upload_profile_pic_api"),
    path("api/signup/", api_signup, name="api_signup"),
    path("logout/", logout_view, name="user_logout"),
    path("test_upload/", test_upload),
    path(
        "api/invite/<str:username>/",
        InviteListView.as_view(),
        name="invite_user_api_other",
    ),
    path("api/invite/", InviteListView.as_view(), name="invite_user_api"),
    path("api/pending_invite/", api_pending_invite, name="pending_invite_api"),
    path("api/friends/", FriendListView.as_view(), name="friends_user_api"),
    path(
        "api/friends/<str:username>/",
        FriendListView.as_view(),
        name="friends_user_api_other",
    ),
    path("api/blocked/", BlockedListView.as_view(), name="blocked_user_api"),
    path(
        "api/blocked/<str:username>/",
        BlockedListView.as_view(),
        name="blocked_user_api_other",
    ),
    path(
        "api/search/<str:username>/", search_usernames_api, name="search_usernames_api"
    ),
    path(
        "api/profile/<str:username>/", profile_info_api, name="profile_info_api_other"
    ),
    path("api/profile/", profile_info_api, name="profile_info_api"),
    path("api/last_active/<str:username>/", is_active_api, name="is_active_api"),
    path("api/change_password/", change_password_api, name="change_password_api"),
    path(
        "test/change_password/",
        test_password_change_view,
        name="test_password_change_view",
    ),
    path("api/undo_invite/<str:username>/", undo_invite_api, name="undo_invite_api"),
    path("api/exist/<str:username>/", user_exist_api, name="user_exist_api"),
    path("api/is_blocked/<str:username>/", is_blocked_api, name="is_blocked_api"),
    path("api/colors/", ColorView.as_view(), name="color_api"),
]
