import stripe
from django.conf import settings

from .models import OrganisationSubscription

STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY
STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY


def check_and_cancel_inactive_subscription():
    for organisation_subscription in OrganisationSubscription.objects.filter(
        status="ACTIVE"
    ):
        # check on stripe
        if not organisation_subscription.stripe_subscription_id:
            continue

        stripe_subscription_response = stripe.Subscription.retrieve(
            organisation_subscription.stripe_subscription_id
        )
        if stripe_subscription_response.status != "active":
            organisation_subscription.status = "INACTIVE"
            organisation_subscription.save()

    return
