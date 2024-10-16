from django import forms

from rabah_dashboard.models import ContactUs


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ["name", "email", 'mobile', "message"]
