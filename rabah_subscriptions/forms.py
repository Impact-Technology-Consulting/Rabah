import pycountry
from django import forms

from rabah_subscriptions.models import BillingAddress


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ('address', 'city', 'state', 'country', 'zip_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate the choices for the country field
        self.fields['country'] = forms.ChoiceField(choices=self.get_country_choices())

    def get_country_choices(self):
        # Get a list of country codes and names from pycountry
        country_choices = [(country.alpha_2, country.name) for country in pycountry.countries]
        # Sort the list alphabetically by country name
        country_choices.sort(key=lambda x: x[1])
        return country_choices
