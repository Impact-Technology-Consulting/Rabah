import uuid

from django.db import models
from django.db.models.signals import post_save

from rabah_members.models import Member
from rabah_organisations.models import Organisation

# Create your models here.
SUBSCRIPTION_STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
)


class Subscription(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=250, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class BillingAddress(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    organisation = models.ForeignKey(
        Organisation, on_delete=models.SET_NULL, blank=True, null=True
    )
    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    zip_code = models.CharField(max_length=250, blank=True, null=True)
    is_billing_verified = models.BooleanField(default=False)
    is_card_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class OrganisationSubscription(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, blank=True, null=True
    )
    billing_subscription = models.ForeignKey(
        BillingAddress, on_delete=models.SET_NULL, blank=True, null=True
    )
    organisation = models.ForeignKey(
        Organisation, on_delete=models.SET_NULL, blank=True, null=True
    )
    status = models.CharField(choices=SUBSCRIPTION_STATUS, max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)


def post_save_create_organisation(sender, instance, *args, **kwargs):
    """
    This creates a user  profile once a user is being created
    :param instance:  the user created or updated
    """
    if instance:
        organisation_subscription = OrganisationSubscription.objects.filter(
            organisation=instance
        ).first()
        if not organisation_subscription:
            OrganisationSubscription.objects.create(
                organisation=instance, status="INACTIVE"
            )


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
