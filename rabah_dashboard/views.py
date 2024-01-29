from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from rabah_contributions.models import Contribution, ContributionType
from rabah_contributions.utils import total_contribution_amount
from rabah_events.models import Event
from rabah_members.models import Member
from rabah_organisations.models import Group
from users.mixin import AuthAndOrganizationMixin


class RabahHomePageView(View):
    def get(self, request):
        return render(request, "home/index.html")


class UserOrganisationsView(LoginRequiredMixin, View):
    def get(self, request):
        member = Member.objects.filter(user=self.request.user)
        return render(request, "dashboard/organisation_list.html", {"members": member})


class DashBoardView(AuthAndOrganizationMixin, View):
    def get(self, request):
        organisation_id = request.COOKIES.get("organisation_id")
        if not organisation_id:
            # Handle the case where organization ID is not set
            return redirect("rabah_dashboard:user_organisations")

        member = Member.objects.filter(
            user=self.request.user, organisation_id=organisation_id
        ).first()
        groups_count = Group.objects.filter(organisation_id=organisation_id).count()
        groups = Group.objects.filter(organisation_id=organisation_id)
        events = Event.objects.filter(organisation_id=organisation_id).count()
        members_count = Member.objects.filter(organisation_id=organisation_id).count()
        members = Member.objects.filter(organisation_id=organisation_id)
        contribution_types = ContributionType.objects.filter(
            organisation_id=organisation_id
        )[:5]
        contributions = Contribution.objects.filter(organisation_id=organisation_id)[:5]
        total_contributions = total_contribution_amount(self.organisation_id)
        context = {
            "groups_count": groups_count,
            "members_count": members_count,
            "groups": groups,
            "members": members,
            "contribution_types": contribution_types,
            "contributions": contributions,
            "total_contributions": total_contributions,
            "events": events,
        }

        return render(request, "dashboard/dashboard.html", context)
