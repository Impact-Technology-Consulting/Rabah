from django.urls import path

from rabah_organisations.views import GroupListView, GroupUpdateView, GroupDetailView, GroupDeleteView

app_name = "rabah_organisations"
urlpatterns = [
    path("groups/", GroupListView.as_view(), name="groups"),
    path("groups/<str:id>/", GroupDetailView.as_view(), name="groups_detail"),
    path("group_update/<str:id>/", GroupUpdateView.as_view(), name="groups_update"),
    path("group_delete/<str:id>/", GroupDeleteView.as_view(), name="group_delete"),
]
