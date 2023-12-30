from django.urls import path

from .views import DashBoardView, UserOrganisationsView, RabahHomePageView

app_name = "rabah_dashboard"
urlpatterns = [
    path("", RabahHomePageView.as_view(), name="home_page"),
    path("dashbaord", DashBoardView.as_view(), name="dashboard"),
    path("user_organisations", UserOrganisationsView.as_view(), name="user_organisations"),
]
