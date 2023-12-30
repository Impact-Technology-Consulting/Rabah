from django import forms

from rabah_subscriptions.models import BillingAddress


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ('address', 'city', 'state', 'country', 'zip_code')
