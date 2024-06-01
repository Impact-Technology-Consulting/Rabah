import stripe
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from rabah_members.utils import get_member
from rabah_subscriptions.forms import BillingAddressForm
from rabah_subscriptions.models import BillingAddress, Subscription, PromoCode
from rabah_subscriptions.models import OrganisationSubscription
from users.mixin import AuthAndAdminOrganizationNotSubscribedMixin

STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY
STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC_KEY


class SubscriptionPageView(AuthAndAdminOrganizationNotSubscribedMixin, View):
    """
    this is used to show the current subscription of the organization
    """

    def get(self, request):
        subscriptions = Subscription.objects.all()
        organisation_subscription = OrganisationSubscription.objects.filter(
            organisation_id=self.organisation_id
        ).first()
        if not organisation_subscription:
            organisation_subscription = OrganisationSubscription.objects.create(
                organisation_id=self.organisation_id, status="INACTIVE"
            )

        context = {
            "organisation_subscription": organisation_subscription,
            "subscriptions": subscriptions,
        }
        return render(request, "dashboard/subscription.html", context)


class AddBillingCardView(AuthAndAdminOrganizationNotSubscribedMixin, View):
    """
    this is used to add the billing card details
    """

    def get(self, request, subscription_id):
        member = get_member(self.request.user, self.organisation_id)
        if not member:
            return render(request, "404.html")
        billing_address, created = BillingAddress.objects.get_or_create(
            organisation=member.organisation
        )
        billing_address_form = BillingAddressForm(instance=billing_address)

        subscription = Subscription.objects.filter(id=subscription_id).first()
        if not subscription:
            messages.warning(request, "Subscription not found")
            return redirect("rabah_subscriptions:subscription_page")

        organisation_subscription = OrganisationSubscription.objects.filter(
            organisation_id=self.organisation_id
        ).first()
        if not organisation_subscription:
            organisation_subscription = OrganisationSubscription.objects.create(
                organisation_id=self.organisation_id
            )

        context = {
            "stripe_public_key": STRIPE_PUBLIC_KEY,
            "billing_address_form": billing_address_form,
            "subscription_id": subscription_id,
        }

        return render(request, "account/account_checkout.html", context)

    def post(self, request, subscription_id):
        member = get_member(self.request.user, self.organisation_id)
        if not member:
            return render(request, "404.html")

        subscription = Subscription.objects.filter(id=subscription_id).first()
        if not subscription:
            messages.warning(request, "Subscription not found")
            return redirect("rabah_subscriptions:subscription_page")

        organisation_subscription = OrganisationSubscription.objects.filter(
            organisation_id=self.organisation_id
        ).first()
        if not organisation_subscription:
            organisation_subscription = OrganisationSubscription.objects.create(
                organisation_id=self.organisation_id
            )

        billing_address, created = BillingAddress.objects.get_or_create(
            organisation=member.organisation
        )

        form = BillingAddressForm(instance=billing_address, data=self.request.POST)
        stripeToken = self.request.POST.get("stripeToken")
        if not stripeToken:
            messages.warning(request, "stripe card not provided or invalid token")
            return redirect("rabah_subscriptions:billing_card")

        coupon = self.request.POST.get("coupon")


        if form.is_valid():
            form.save()
            billing_address.is_billing_verified = True
            billing_address.save()
            if coupon:
                promo_code = PromoCode.objects.filter(code=coupon).first()
                if promo_code and promo_code.promo_code_is_valid():
                    billing_address.promo_code = promo_code
                    billing_address.save()

            try:
                customer = stripe.Customer.retrieve(organisation_subscription.stripe_customer_id)
                customer.source = stripeToken
                customer.save()

                # subscribe to a subscription by returning to the make payment page
                messages.success(request, "Successfully updated billing info and card")

                return redirect("rabah_subscriptions:make_payment", subscription_id)

            except stripe.error.CardError as e:
                # The card has been declined
                messages.warning(request, f"Card declined: {e.error.message}")
                return redirect("rabah_subscriptions:billing_card", subscription_id)

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                messages.warning(
                    request, f"Invalid request to Stripe API: {e.error.message}"
                )
                return redirect("rabah_subscriptions:billing_card", subscription_id)

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                messages.warning(
                    request, f"Authentication error with Stripe: {e.error.message}"
                )
                return redirect("rabah_subscriptions:billing_card", subscription_id)

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(
                    request, f"Network error with Stripe API: {e.error.message}"
                )
                return redirect("rabah_subscriptions:billing_card", subscription_id)

            except stripe.error.StripeError as e:
                # Something else happened, completely unrelated to Stripe
                messages.warning(request, f"Stripe error occurred: {e.error.message}")
                return redirect("rabah_subscriptions:billing_card", subscription_id)
            except Exception as a:
                messages.warning(request, f"error occurred: {a}")
                return redirect("rabah_subscriptions:billing_card", subscription_id)

        for error in form.errors:
            messages.warning(request, f"{error}: {form.errors[error][0]}")
        return redirect("rabah_subscriptions:billing_card", subscription_id)


class PaymentView(AuthAndAdminOrganizationNotSubscribedMixin, View):
    """
    this is used to view current plan or payment and also page to cancel the subscription
    """

    def get(self, request, subscription_id):
        subscription = Subscription.objects.filter(id=subscription_id).first()
        if not subscription:
            messages.warning(request, "Subscription not found")
            return redirect("rabah_subscriptions:subscription_page")
        organisation_subscription = OrganisationSubscription.objects.filter(
            organisation_id=self.organisation_id
        ).first()
        if not organisation_subscription:
            organisation_subscription = OrganisationSubscription.objects.create(
                organisation_id=self.organisation_id
            )

        billing_address, created = BillingAddress.objects.get_or_create(
            organisation_id=self.organisation_id
        )

        #  commented  this and added it on  the make payment page
        # stripe_customer = stripe.Customer.retrieve(
        #     organisation_subscription.stripe_customer_id
        # )
        # if not stripe_customer.default_source:
        #     messages.warning(request, "No card found for this organisation")
        #     return redirect("rabah_subscriptions:billing_card", subscription_id)

        # if the subscription id is trail and the user have the promocode and also the user have not used the trial add the user to the trial
        if (
                subscription.subscription_duration == "14_DAYS_TRIAL"
                and organisation_subscription.organisation.has_trial
        ):
            if not organisation_subscription.subscription:
                return redirect("rabah_subscriptions:make_payment", subscription_id)

        context = {
            "subscription": subscription,
            "organisation_subscription": organisation_subscription,
            "billing_address": billing_address,
        }
        return render(request, "dashboard/make_payment.html", context)


class MakePaymentView(AuthAndAdminOrganizationNotSubscribedMixin, View):
    """
    this is used to make payment for the subscription
    """

    def get(self, request, subscription_id):
        subscription = Subscription.objects.filter(id=subscription_id).first()
        if not subscription:
            messages.warning(request, "Subscription not found")
            return redirect("rabah_subscriptions:subscription_page")

        billing_info = BillingAddress.objects.filter(organisation_id=self.organisation_id).first()
        if not billing_info:
            return redirect("rabah_subscriptions:billing_card", subscription_id)


        organisation_subscription = OrganisationSubscription.objects.filter(
            organisation_id=self.organisation_id
        ).first()
        if not organisation_subscription:
            organisation_subscription = OrganisationSubscription.objects.create(
                organisation_id=self.organisation_id
            )


        stripe_customer = stripe.Customer.retrieve(
            organisation_subscription.stripe_customer_id
        )
        if not stripe_customer.default_source:
            messages.warning(request, "No card found for this organisation")
            return redirect("rabah_subscriptions:billing_card", subscription_id)


        try:
            #  charge the card
            customer = stripe.Customer.retrieve(
                organisation_subscription.stripe_customer_id
            )

            if subscription.subscription_duration == "14_DAYS_TRIAL":
                if organisation_subscription.stripe_subscription_id:
                    messages.warning(request, "you already exceeded your 14 days trial")
                    return redirect("rabah_subscriptions:subscription_page")
                stripe_subscription = stripe.Subscription.create(
                    customer=customer.id,
                    cancel_at_period_end=True,
                    items=[
                        {
                            "price": subscription.stripe_plan_id,
                        },
                    ],
                )
            else:
                # Prepare subscription data
                subscription_data = {
                    "customer": customer.id,
                    "items": [{"price": subscription.stripe_plan_id}],
                }

                # Check if a promo code exists and apply it to the subscription data
                if billing_info.promo_code:
                    if billing_info.promo_code.promo_code_is_valid():
                        subscription_data["coupon"] = billing_info.promo_code.code
                        messages.success(request, "Promo code applied successfully")

                stripe_subscription = stripe.Subscription.create(**subscription_data)

            # update the organization
            organisation_subscription.subscription_id = subscription_id
            organisation_subscription.stripe_subscription_id = stripe_subscription.id
            organisation_subscription.status = "ACTIVE"
            organisation_subscription.save()


            messages.success(request, "Successfully make payment for subscription ")
            return redirect("rabah_subscriptions:payment", subscription_id)

        except stripe.error.CardError as e:
            # The card has been declined
            messages.warning(request, f"Card declined: {e.error.message}")
            return redirect("rabah_subscriptions:billing_card", subscription_id)

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(
                request, f"Invalid request to Stripe API: {e.error.message}"
            )
            return redirect("rabah_subscriptions:billing_card", subscription_id)

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            messages.warning(
                request, f"Authentication error with Stripe: {e.error.message}"
            )
            return redirect("rabah_subscriptions:billing_card", subscription_id)

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(
                request, f"Network error with Stripe API: {e.error.message}"
            )
            return redirect("rabah_subscriptions:billing_card", subscription_id)

        except stripe.error.StripeError as e:
            # Something else happened, completely unrelated to Stripe
            messages.warning(request, f"Stripe error occurred: {e.error.message}")
            return redirect("rabah_subscriptions:billing_card", subscription_id)


class CancelPaymentView(AuthAndAdminOrganizationNotSubscribedMixin, View):
    """
    this is used to cancel the subscription
    """

    def get(self, request, subscription_id):
        subscription = Subscription.objects.filter(id=subscription_id).first()
        if not subscription:
            messages.warning(request, "Subscription not found")
            return redirect("rabah_subscriptions:subscription_page")

        organisation_subscription = OrganisationSubscription.objects.filter(
            organisation_id=self.organisation_id
        ).first()
        if not organisation_subscription:
            organisation_subscription = OrganisationSubscription.objects.create(
                organisation_id=self.organisation_id
            )

        if (
                not organisation_subscription.stripe_subscription_id
                or organisation_subscription.status == "INACTIVE"
        ):
            messages.warning(request, "No subscription found for this organisation")
            return redirect("rabah_subscriptions:subscription_page")

        stripe_subscription = stripe.Subscription.retrieve(
            organisation_subscription.stripe_subscription_id
        )
        stripe_subscription.delete()

        #  set the subscription to be inactive
        organisation_subscription.stripe_subscription_id = ""
        organisation_subscription.status = "INACTIVE"
        organisation_subscription.save()

        messages.success(
            request, f"Successfully cancelled {subscription.name} subscription"
        )
        return redirect("rabah_subscriptions:subscription_page")


class PromoCodeValidateAPIView(AuthAndAdminOrganizationNotSubscribedMixin, View):
    """
    this is used to validate the promo code subscription
    """

    def get(self, request):
        coupon = self.request.GET.get("coupon")
        if not coupon:
            return JsonResponse({"error": "promo code is required"}, status=400)
        promo_code_instance = PromoCode.objects.filter(code=coupon).first()
        if not promo_code_instance:
            return JsonResponse({"error": "promo code not found"}, status=400)
        if promo_code_instance.expiration_date <= timezone.now():
            return JsonResponse({"error": "promo code is expired"}, status=400)
        return JsonResponse({"success": "promo code is valid", "data": {
            "code": promo_code_instance.code,
            "discount_percentage": promo_code_instance.discount_percentage,
            "duration": promo_code_instance.duration,
            "expiration_date": promo_code_instance.expiration_date,
        }}, status=200)

