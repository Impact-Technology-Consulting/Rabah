from django import forms
from django.forms import DateTimeInput

from rabah_events.models import Event


class EventCreateForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    end_date = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
        ]

    def __init__(self, organisation_id, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
        self.fields['organisation_id'] = forms.CharField(widget=forms.HiddenInput(), initial=organisation_id)

    def save(self, commit=True):
        instance = super(EventCreateForm, self).save(commit=False)
        instance.organisation_id = self.cleaned_data['organisation_id']
        if commit:
            instance.save()
        return instance
