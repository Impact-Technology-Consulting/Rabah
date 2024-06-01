import uuid

import stripe
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from rabah_members.models import Member
from rabah_organisations.models import Organisation
from django.utils import timezone

# Create your models here.
SUBSCRIPTION_STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
)
SUBSCRIPTION_DURATION = (
    ("14_DAYS_TRIAL", "14_DAYS_TRIAL"),
    ("MONTHLY", "MONTHLY"),
    ("QUARTERLY", "QUARTERLY"),
    ("YEARLY", "YEARLY"),
)

stripe.api_key = settings.STRIPE_SECRET_KEY


class Subscription(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=250, blank=True, null=True)
    stripe_plan_id = models.CharField(max_length=250, blank=True, null=True)
    subscription_duration = models.CharField(
        choices=SUBSCRIPTION_DURATION, max_length=250, blank=True, null=True
    )
    #  only used for the trail. The old implementation for promo code
    promo_code = models.CharField(max_length=250, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


def post_save_create_subscription(sender, instance, *args, **kwargs):
    """
    This creates a subscription plan or update the plan from stripe
    """
    if instance:
        subscription = Subscription.objects.filter(id=instance.id).first()
        if subscription:
            if subscription.stripe_plan_id:

                plan_retrieve_response = stripe.Plan.retrieve(
                    subscription.stripe_plan_id
                )
                if plan_retrieve_response.amount != subscription.price:
                    pass
            else:
                # Subscription doesn't exist on Stripe, so create it
                if subscription.subscription_duration == "14_DAYS_TRIAL":
                    interval_count = 14
                    interval = "day"
                elif subscription.subscription_duration == "MONTHLY":
                    interval_count = 1
                    interval = "month"
                elif subscription.subscription_duration == "QUARTERLY":
                    interval_count = 3
                    interval = "month"
                elif subscription.subscription_duration == "YEARLY":
                    interval_count = 1
                    interval = "year"
                else:
                    return

                product_response = stripe.Product.create(
                    name=f"{interval} Subscription"
                )
                if subscription.price <= 0:
                    amount = 0
                else:
                    amount = int(subscription.price * 100)
                plan_response = stripe.Plan.create(
                    amount=amount,  # Amount in cents
                    currency="usd",
                    interval=interval,
                    interval_count=interval_count,
                    product=product_response.id,
                )
                # Update the subscription with the Stripe plan ID
                subscription.stripe_plan_id = plan_response.id
                subscription.save()


post_save.connect(post_save_create_subscription, sender=Subscription)


class BillingAddress(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    organisation = models.ForeignKey(
        Organisation, on_delete=models.SET_NULL, blank=True, null=True
    )
    promo_code = models.ForeignKey("PromoCode",on_delete=models.SET_NULL, blank=True, null=True)

    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    zip_code = models.CharField(max_length=250, blank=True, null=True)
    is_billing_verified = models.BooleanField(default=False)
    is_card_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def billing_and_card_is_verified(self):
        return self.is_billing_verified and self.is_card_verified


class OrganisationSubscription(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, blank=True, null=True
    )
    stripe_customer_id = models.CharField(max_length=250, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=250, blank=True, null=True)
    billing_subscription = models.ForeignKey(
        BillingAddress, on_delete=models.SET_NULL, blank=True, null=True
    )
    organisation = models.OneToOneField(
        Organisation, on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.CharField(choices=SUBSCRIPTION_STATUS, max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)


def post_save_create_organisation(sender, instance, *args, **kwargs):
    """
    This creates a user profile once a user is being created
    :param instance:  the user created or updated
    """
    if instance:
        organisation_subscription = OrganisationSubscription.objects.filter(
            organisation=instance
        ).first()
        if not organisation_subscription:
            organisation_subscription = OrganisationSubscription.objects.create(
                organisation=instance, status="INACTIVE"
            )
        if not organisation_subscription.stripe_customer_id:
            customer_response = stripe.Customer.create(email=instance.owner.email)
            organisation_subscription.stripe_customer_id = customer_response.id
            organisation_subscription.save()


post_save.connect(post_save_create_organisation, sender=Organisation)

TRANSACTION_STATUS = (
    ("SUCCESS", "SUCCESS"),
    ("FAILED", "FAILED"),
)
METHOD_CHOICES = (
    ("CASH", "Cash"),
    ("CREDIT_CARD", "Credit Card"),
    ("DEBIT_CARD", "Debit Card"),
    ("BANK_TRANSFER", "Bank Transfer"),
    ("CHECK", "Check"),
    ("MONEY_ORDER", "Money Order"),
    ("PAYPAL", "PayPal"),
    ("VENMO", "Venmo"),
    ("BITCOIN", "Bitcoin"),
    ("APPLE_PAY", "Apple Pay"),
    ("GOOGLE_PAY", "Google Pay"),
    ("SQUARE", "Square"),
    ("CRYPTOCURRENCY", "Other Cryptocurrency"),
    ("OTHER", "Other"),
)


class Transaction(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    organisation = models.ForeignKey(
        Organisation, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_by = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_by",
    )
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True)
    method = models.CharField(
        max_length=250, choices=METHOD_CHOICES, blank=True, null=True
    )
    transaction_id = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=255, blank=True, null=True, choices=TRANSACTION_STATUS
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_anonymous = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


PROMOCODE_DURATION = (
    ('once', 'Once'),
    ('forever', 'Forever'),
    ('repeating', 'Repeating'),
)

class PromoCode(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.CharField(max_length=50,choices=PROMOCODE_DURATION, default='once')
    expiration_date = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Code: {self.code} -- Discount: {self.discount_percentage}% -- Duration: {self.duration} -- Expiry Date: {self.expiration_date}"


    def promo_code_is_valid(self):
        """
        Check if the promo code is valid
        """
        try:
            coupon = stripe.Coupon.retrieve(self.code)
            if not coupon.redeem_by:
                return False
            if coupon.redeem_by < timezone.now().timestamp():
                return False
            return True
        except :
            return False


@receiver(post_save, sender=PromoCode)
def post_save_create_or_update_promo_code(sender, instance, **kwargs):
    """
    Create or update the promo code on Stripe when a new promo code is created or updated in Django
    """
    if instance:
        try:
            stripe.Coupon.retrieve(instance.code)
            # Update existing coupon
            stripe.Coupon.modify(
                instance.code
            )
        except stripe.error.InvalidRequestError:
            # Create new coupon if it doesn't exist
            stripe.Coupon.create(
                id=instance.code,
                percent_off=instance.discount_percentage,
                duration=instance.duration,
                redeem_by=int(instance.expiration_date.timestamp())
            )


@receiver(post_delete, sender=PromoCode)
def post_delete_promo_code(sender, instance, **kwargs):
    """
    Delete the promo code on Stripe when a promo code is deleted in Django
    """
    try:
        stripe.Coupon.delete(instance.code)
    except stripe.error.InvalidRequestError:
        # The promo code might already be deleted or never existed
        pass

