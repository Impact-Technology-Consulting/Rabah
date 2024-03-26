from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from rabah_contributions.models import Contribution, ContributionType
from rabah_contributions.utils import total_contribution_amount
from rabah_dashboard.forms import ContactUsForm
from rabah_events.models import Event
from rabah_members.models import Member
from rabah_organisations.models import Group, Organisation
from rabah_subscriptions.models import Subscription
from users.mixin import AuthAndOrganizationMixin
from users.models import User


class RabahHomePageView(View):
    def get(self, request):
        event_count = Event.objects.all().count()
        member_count = Member.objects.all().count()
        user_count = User.objects.all().count()
        organisation_count = Organisation.objects.all().count()

        subscription_monthly = Subscription.objects.filter(subscription_duration="MONTHLY").first()
        subscription_quarterly = Subscription.objects.filter(subscription_duration="QUARTERLY").first()
        subscription_yearly = Subscription.objects.filter(subscription_duration="YEARLY").first()

        context = {
            "event_count": event_count,
            "member_count": member_count,
            "user_count": user_count,
            "organisation_count": organisation_count,
            "subscription_monthly": subscription_monthly,
            "subscription_quarterly": subscription_quarterly,
            "subscription_yearly": subscription_yearly,
        }

        return render(request, "landing_page/index.html", context)


class RabahContactUsPageView(View):
    def get(self, request):
        return render(request, "landing_page/contact-us.html")

    def post(self, request):
        form = ContactUsForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message received we would get back to you")
        else:
            messages.error(request, "invalid message provided")

        return redirect("rabah_dashboard:contact_us")


class RabahAboutUsPageView(View):
    def get(self, request):
        return render(request, "landing_page/about-us.html")


class UserOrganisationsView(LoginRequiredMixin, View):

    def get(self, request):
        member = Member.objects.filter(user=self.request.user)
        if member.count() == 1:
            response = redirect("rabah_dashboard:dashboard")
            response.set_cookie('organisation_id', member.first().organisation_id)
            return response

        if member.count() == 0:
            user = self.request.user
            user.delete()
            logout(request)
            messages.error(request, "account have organisation attached to it please signup ")
            return redirect('account_signup')
        return render(request, 'dashboard/organisation_list.html', {"members": member})


class DashBoardView(AuthAndOrganizationMixin, View):

    def get(self, request):
        organisation_id = request.COOKIES.get('organisation_id')
        if not organisation_id:
            # Handle the case where organization ID is not set
            return redirect("rabah_dashboard:user_organisations")

        member = Member.objects.filter(user=self.request.user, organisation_id=organisation_id).first()
        groups_count = Group.objects.filter(organisation_id=organisation_id).count()
        groups = Group.objects.filter(organisation_id=organisation_id)
        events = Event.objects.filter(organisation_id=organisation_id).count()

        members_count = Member.objects.filter(organisation_id=organisation_id).count()
        members = Member.objects.filter(organisation_id=organisation_id)

        contribution_types = ContributionType.objects.filter(organisation_id=organisation_id)[:5]
        contributions = Contribution.objects.filter(organisation_id=organisation_id)[:5]
        total_contributions = total_contribution_amount(self.organisation_id)

        event_increment_percentage = Event.objects.calculate_event_increment_percentage(self.organisation_id)
        contribution_increment_percentage = Contribution.objects.calculate_contribution_increment_percentage(
            self.organisation_id)
        member_increment_percentage = Member.objects.calculate_member_increment_percentage(self.organisation_id)
        group_increment_percentage = Group.objects.calculate_group_increment_percentage(self.organisation_id)
        context = {
            "groups_count": groups_count,
            "members_count": members_count,
            "groups": groups,
            "members": members,
            "contribution_types": contribution_types,
            "contributions": contributions,
            "total_contributions": total_contributions,
            "events": events,
            "member_increment_percentage": round(member_increment_percentage, 2),
            "group_increment_percentage": round(group_increment_percentage, 2),
            "contribution_increment_percentage": round(contribution_increment_percentage, 2),
            "event_increment_percentage": round(event_increment_percentage, 2),
        }

        return render(request, 'dashboard/dashboard.html', context)
