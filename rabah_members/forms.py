from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from rabah_members.models import Member
from rabah_organisations.models import Group
from users.models import GENDER_CHOICES, User
from .models import FAMILY_RELATIONSHIP_CHOICES


class MemberCreateForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    mobile = forms.IntegerField()
    address = forms.CharField(max_length=150)
    career = forms.CharField(max_length=150)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False, widget=CheckboxSelectMultiple)

    def __init__(self, organisation_id, *args, **kwargs):
        super(MemberCreateForm, self).__init__(*args, **kwargs)
        self.fields['organisation_id'] = forms.CharField(widget=forms.HiddenInput(), initial=organisation_id)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if the email is already used
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use. Please use a different email.')

        return email

    def save(self, commit=True):
        user = User.objects.create(
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            mobile=self.cleaned_data['mobile']
        )
        try:
            instance = Member()
            user_profile = user.user_profile
            user_profile.address = self.cleaned_data['address']
            user_profile.career = self.cleaned_data['career']
            user_profile.gender = self.cleaned_data["gender"]
            user_profile.save()
            instance.organisation_id = self.cleaned_data['organisation_id']
            instance.user = user
            instance.save()

            instance.groups.set(self.cleaned_data['groups'])
            if commit:
                instance.save()
            return instance
        except:
            user.delete()
        return None


class MemberEditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['family',
                  'family_relationship', 'is_admin_member', 'is_owner', 'is_active', 'groups']
        widgets = {
            'groups': CheckboxSelectMultiple(),
        }


class AddExistingMemberToFamilyForm(forms.Form):
    family_relationship = forms.ChoiceField(choices=FAMILY_RELATIONSHIP_CHOICES)
    new_member_id = forms.UUIDField(widget=forms.HiddenInput)
    new_member_name = forms.CharField(max_length=250)

    def __init__(self, organisation_id, current_member_id, *args, **kwargs):
        super(AddExistingMemberToFamilyForm, self).__init__(*args, **kwargs)
        self.fields['current_member_id'] = forms.CharField(widget=forms.HiddenInput(), initial=current_member_id)
        self.fields['organisation_id'] = forms.CharField(widget=forms.HiddenInput(), initial=organisation_id)

    def save(self):
        current_member = Member.objects.filter(id=self.cleaned_data["current_member_id"],
                                               organisation_id=self.cleaned_data["organisation_id"]).first()
        if not current_member:
            return None
        if not current_member.family:
            current_member.create_family()
        new_member = Member.objects.filter(id=self.cleaned_data["new_member_id"],
                                           organisation_id=self.cleaned_data["organisation_id"]).first()
        if not new_member:
            return None
        if new_member.family == current_member.family:
            return None
        new_member.family = current_member.family
        new_member.save()
        return new_member


class UpdateExistingMemberFamilyRelationShipForm(forms.Form):
    """
    this is used to update the existing member family relationship
    """
    family_relationship = forms.ChoiceField(choices=FAMILY_RELATIONSHIP_CHOICES)
    family_relationship_member_id = forms.UUIDField()

    def save(self):
        member = Member.objects.filter(id=self.cleaned_data["family_relationship_member_id"]).first()
        if not member:
            return None
        member.family_relationship = self.cleaned_data["family_relationship"]
        member.save()
        return member
