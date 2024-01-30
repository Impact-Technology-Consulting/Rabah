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
    repeat_until_date = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    # Define choices for repeat_count dynamically
    REPEAT_COUNT_CHOICES = [(i, f"{i} event's") for i in range(1, 101)]

    repeat_count = forms.ChoiceField(
        choices=REPEAT_COUNT_CHOICES,
        initial=1,  # Set the default value to 1
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Event
        fields = [
            "name",
            "image",
            "description",
            "start_date",
            "end_date",
            "repeat",
            "repeat_end",
            "repeat_count",
            "repeat_until_date",
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
