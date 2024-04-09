from django.urls import path

from .views import (
    DashBoardView,
    UserOrganisationsView,
    RabahHomePageView,
    RabahContactUsPageView,
    RabahAboutUsPageView,
)

app_name = "rabah_dashboard"
urlpatterns = [
    path("", RabahHomePageView.as_view(), name="home_page"),
    path("contact_us/", RabahContactUsPageView.as_view(), name="contact_us"),
    path("about_us/", RabahAboutUsPageView.as_view(), name="about_us"),
    path("dashbaord/", DashBoardView.as_view(), name="dashboard"),
    path(
        "user_organisations/",
        UserOrganisationsView.as_view(),
        name="user_organisations",
    ),
]
