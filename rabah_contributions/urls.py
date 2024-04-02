from django.urls import path

from .views import (
    GivingContributionView,
    ContributionTypeView,
    ContributionTypeUpdateView,
    ContributionTypeDeleteView,
    ContributionsView,
    ContributionDeleteView,
    ContributionUpdateView,
)

app_name = "rabah_contributions"
urlpatterns = [
    path(
        "add_contribution_type",
        ContributionTypeView.as_view(),
        name="add_contribution_type",
    ),
    path(
        "update_contribution_type/<str:contribution_type_id>/",
        ContributionTypeUpdateView.as_view(),
        name="update_contribution_type",
    ),
    path(
        "delete_contribution_type/<str:contribution_type_id>/",
        ContributionTypeDeleteView.as_view(),
        name="delete_contribution_type",
    ),
    path(
        "contributions/<str:contribution_type_id>/",
        ContributionsView.as_view(),
        name="contributions",
    ),
    path(
        "contribution_delete/<str:contribution_id>/",
        ContributionDeleteView.as_view(),
        name="contribution_delete",
    ),
    path(
        "add_giving_transaction",
        GivingContributionView.as_view(),
        name="add_giving_transaction",
    ),
    path(
        "contribution_update/<str:contribution_id>",
        ContributionUpdateView.as_view(),
        name="contribution_update",
    ),
]
