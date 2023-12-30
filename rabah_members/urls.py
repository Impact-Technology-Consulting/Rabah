from django.urls import path

from .views import MembersDashboardView, GroupMembersView, MemberDetailView, AdminAddMemberPageView, \
    AddFamilyMemberView, MemberAutocompleteView, AddExistingMemberToFamilyView, \
    UpdateExistingMemberFamilyRelationShipView

app_name = "rabah_members"
urlpatterns = [
    path("members/", MembersDashboardView.as_view(), name="members"),
    path('autocomplete/', MemberAutocompleteView.as_view(), name='member_autocomplete'),
    path("add_member/", AdminAddMemberPageView.as_view(), name="add_member"),
    path("add_member/<str:member_id>/", AddFamilyMemberView.as_view(), name="add_family_member"),
    path("add_existing_member_to_family/<str:member_id>/", AddExistingMemberToFamilyView.as_view(),
         name="add_existing_member_to_family"),
    path("update_existing_member_to_family/", UpdateExistingMemberFamilyRelationShipView.as_view(),
         name="update_existing_member_to_family"),

    path("members/<str:group_id>/", GroupMembersView.as_view(), name="group_members"),
    path("member_detail/<str:id>/", MemberDetailView.as_view(), name="group_member_detail"),
]
