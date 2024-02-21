from django.urls import path

from .views import AddBillingCardView, SubscriptionPageView, MakePaymentView, CancelPaymentView, PaymentView

app_name = "rabah_subscriptions"
urlpatterns = [
    path("subscription_page", SubscriptionPageView.as_view(), name="subscription_page"),
    path("billing_card/<str:subscription_id>/", AddBillingCardView.as_view(), name="billing_card"),
    path("payment/<str:subscription_id>/", PaymentView.as_view(), name="payment"),
    path("make_payment/<str:subscription_id>/", MakePaymentView.as_view(), name="make_payment"),
    path("cancel_subscription/<str:subscription_id>/", CancelPaymentView.as_view(), name="cancel_subscription"),

]
