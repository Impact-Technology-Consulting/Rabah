from decouple import config
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from users.views import RabahSignupView, RabahLoginView

admin_url = config("ADMIN_URL", default="admin_dont_url")

urlpatterns = [
    path(f"{admin_url}/", admin.site.urls, name="admin"),
    path("users/", include("users.urls"), name="users"),
    path("", include("rabah_dashboard.urls"), name="rabah_dashboard"),
    path(
        "organisations/",
        include("rabah_organisations.urls"),
        name="rabah_organisations",
    ),
    path("member/", include("rabah_members.urls"), name="rabah_members"),
    path(
        "rabah_contributions/",
        include("rabah_contributions.urls"),
        name="rabah_contributions",
    ),
    path("event/", include("rabah_events.urls"), name="rabah_events"),
    path(
        "subscription/", include("rabah_subscriptions.urls"), name="rabah_subscriptions"
    ),
    path("accounts/login/", RabahLoginView.as_view(), name="account_login"),
    path("accounts/signup/", RabahSignupView.as_view(), name="account_signup"),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
