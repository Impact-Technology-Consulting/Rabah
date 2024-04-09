from django.urls import path

from .views import UserProfileView, ChangeUserPassword, CustomLogout, MemberUserProfileUpdateView, \
    MemberCreatePasswordView, SetTimeZone

app_name = "user"
urlpatterns = [
    path("user_profile/", UserProfileView.as_view(), name="user_profile"),
    path("member_profile_edit/<str:profile_id>/", MemberUserProfileUpdateView.as_view(), name="member_profile_edit"),
    path("change_user_password/", ChangeUserPassword.as_view(), name="change_user_password"),

    # change user password when login
    path("member_create_password/<str:token>/", MemberCreatePasswordView.as_view(), name="member_create_password"),

    # member invited to an organisation and need to create a password
    path("custom_logout", CustomLogout.as_view(), name="custom_logout"),
    path("set_timezone", SetTimeZone.as_view(), name="set_timezone"),
]
