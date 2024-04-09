from django.contrib import admin

from .models import Subscription, BillingAddress, OrganisationSubscription, Transaction


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("name", "subscription_duration", "price", "timestamp")
    search_fields = ("name", "subscription_duration")
    list_filter = ("subscription_duration", "timestamp")


@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "organisation",
        "address",
        "city",
        "state",
        "country",
        "zip_code",
        "is_billing_verified",
        "is_card_verified",
        "timestamp",
    )
    search_fields = (
        "organisation__name",
        "address",
        "city",
        "state",
        "country",
        "zip_code",
    )
    list_filter = ("is_billing_verified", "is_card_verified", "timestamp")


@admin.register(OrganisationSubscription)
class OrganisationSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("organisation", "subscription", "status", "timestamp")
    search_fields = ("organisation__name", "subscription__name", "status")
    list_filter = ("status", "timestamp")
    readonly_fields = ("stripe_customer_id",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "organisation",
        "created_by",
        "member",
        "method",
        "transaction_id",
        "description",
        "status",
        "amount",
        "timestamp",
    )
    search_fields = (
        "organisation__name",
        "created_by__username",
        "member__username",
        "method",
        "transaction_id",
        "description",
        "status",
    )
    list_filter = ("method", "status", "timestamp")
