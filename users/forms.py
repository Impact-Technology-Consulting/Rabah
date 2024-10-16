from allauth.account.forms import SignupForm
from django import forms
from django.core.exceptions import ValidationError

from users.models import UserProfile, User


class RabahSignupForm(SignupForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": ("Email address"),
                "autocomplete": "email",
            }
        )
    )
    organisation_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField()
    promo_code = forms.CharField(max_length=150, required=False)
    invitation_id = forms.UUIDField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = None


class RabahLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    mobile = forms.IntegerField(required=False)
    email = forms.EmailField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    profile_image = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "career",
            "address",
            "date_of_birth",
            "gender",
            "profile_image",
            "about",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data["email"]
        if self.instance.user.email != email:
            if User.objects.filter(email=email).exists():
                raise ValidationError("This email is already taken.")
        return email

    def save(self, commit=True):
        user = self.instance.user
        user.email = self.cleaned_data["email"]
        user.mobile = self.cleaned_data["mobile"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        if commit:
            self.instance.save()
        return self.instance


class ChangePasswordForm(forms.Form):
    password = forms.SlugField()
    confirm_password = forms.SlugField()
