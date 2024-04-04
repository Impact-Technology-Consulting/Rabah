from django import forms

from .models import Contribution, ContributionType


class ContributionTypeForm(forms.ModelForm):
    class Meta:
        model = ContributionType
        fields = [
            "name",
        ]


class ContributionForm(forms.ModelForm):
    member_name = forms.CharField(max_length=250, required=False)
    member_id = forms.UUIDField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Contribution
        fields = [
            "contribution_type",
            "member_id",
            "member_name",
            "amount",
            "method",
            "description",
            "is_anonymous",
        ]

    def __init__(self, organisation_id, *args, **kwargs):
        super(ContributionForm, self).__init__(*args, **kwargs)
        # Filter contribution types based on the organization
        self.fields['contribution_type'].queryset = ContributionType.objects.filter(organisation_id=organisation_id)


    def save(self, commit=True):
        is_anonymous = self.cleaned_data.get("is_anonymous")
        instance = super().save(commit=False)

        if not is_anonymous:
            instance.member_id = self.cleaned_data.get("member_id")

        if commit:
            instance.save()

        return instance
