from django.shortcuts import render, redirect
from django.views import View

from rabah_members.utils import get_member
from rabah_subscriptions.forms import BillingAddressForm
from users.mixin import AuthAndAdminOrganizationNotSubscribedMixin
from .models import BillingAddress
from .models import OrganisationSubscription


class BillingInfoView(AuthAndAdminOrganizationNotSubscribedMixin, View):
    """
    This is used to display the billing information
    """

    def get(self, request, *args, **kwargs):
        member = get_member(self.request.user, self.organisation_id)
        if not member:
            return render(request, "404.html")

        billing_address, created = BillingAddress.objects.get_or_create(
            organisation=member.organisation
        )
        billing_address_form = BillingAddressForm(instance=billing_address)

        if billing_address.is_billing_verified:
            return redirect("rabah_dashboard:dashboard")
        return render(
            request, "dashboard/billing_info.html", {"form": billing_address_form}
        )

    def post(self, request, *args, **kwargs):
        member = get_member(self.request.user, kwargs.get("organisation_id"))
        if not member:
            return render(request, "404.html")
        billing_address, created = BillingAddress.objects.get_or_create(
            organisation=member.organisation
        )

        form = BillingAddressForm(instance=billing_address, data=self.request.POST)
        if form.is_valid():
            form.save()
            billing_address.is_billing_verified = True
            billing_address.save()
            return redirect("rabah_subscriptions:billing_card")
        return redirect("rabah_subscriptions:billing_info")


class BillingCardView(AuthAndAdminOrganizationNotSubscribedMixin, View):
    """
    this is used to add the billing card details
    """

    def get(self, request, *args, **kwargs):
        member = get_member(self.request.user, self.organisation_id)
        if not member:
            return render(request, "404.html")
        billing_address, created = BillingAddress.objects.get_or_create(
            organisation=member.organisation
        )
        billing_address_form = BillingAddressForm(instance=billing_address)

        if not billing_address.is_billing_verified:
            return redirect("rabah_subscriptions:billing_info")
        return render(request, "dashboard/checkout.html")


class SubscriptionPageView(AuthAndAdminOrganizationNotSubscribedMixin, View):
    """
    this is used to show the current suvscription of the orgainsation
    """

    def get(self, request):
        organisation_subscription = OrganisationSubscription.objects.filter(
            organisation_id=self.organisation_id
        ).first()
        if not organisation_subscription:
            organisation_subscription = OrganisationSubscription.objects.create(
                organisation_id=self.organisation_id, status="INACTIVE"
            )
        context = {"organisation_subscription": organisation_subscription}
        return render(request, "dashboard/subscription.html", context)
