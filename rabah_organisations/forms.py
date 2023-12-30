from django import forms

from rabah_organisations.models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'image', 'description']

    def __init__(self, organisation_id, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['organisation_id'] = forms.CharField(widget=forms.HiddenInput(), initial=organisation_id)

    def save(self, commit=True):
        instance = super(GroupForm, self).save(commit=False)
        instance.organisation_id = self.cleaned_data['organisation_id']
        if commit:
            instance.save()
        return instance
