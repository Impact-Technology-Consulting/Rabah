from django.urls import path

from .views import BillingInfoView, BillingCardView, SubscriptionPageView

app_name = "rabah_subscriptions"
urlpatterns = [
    path("billing_info", BillingInfoView.as_view(), name="billing_info"),
    path("billing_card", BillingCardView.as_view(), name="billing_card"),
    path("subscription_page", SubscriptionPageView.as_view(), name="subscription_page"),

]
