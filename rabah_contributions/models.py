import uuid

from django.db import models

from rabah_members.models import Member
from rabah_organisations.models import Organisation


# Create your models here.


class ContributionType(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def get_amount_contributed(self):
        amount = 0
        for item in self.contribution_set.all():
            amount += item.amount
        return amount

    def total_contribution_amount(self, organisation_id):
        contributions = Contribution.objects.filter(organisation_id=organisation_id)
        total_amount = contributions.aggregate(models.Sum("amount"))["amount__sum"] or 0
        return total_amount


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


class Contribution(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    contribution_type = models.ForeignKey(ContributionType, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="contribution_created_by",
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="contribution_memeber",
    )
    method = models.CharField(
        max_length=250, choices=METHOD_CHOICES, blank=True, null=True
    )
    transaction_id = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_anonymous = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
