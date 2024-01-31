from datetime import datetime

from django import forms
from django.forms import DateTimeInput, DateInput

from rabah_events.models import Event


class EventCreateForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    end_date = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    repeat_until_date = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),
        required=False
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

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        repeat_until_date = cleaned_data.get("repeat_until_date")

        # Validate that start_date is before end_date
        if start_date and end_date and start_date >= end_date:
            self.add_error("end_date", "End date must be after start date.")

        # Validate that repeat_until_date is after start_date
        if repeat_until_date and start_date and repeat_until_date <= start_date.date():
            self.add_error("repeat_until_date", "Repeat until date must be after start date.")

        # Validate that repeat_until_date is not in the past
        if repeat_until_date and repeat_until_date < datetime.now().date():
            self.add_error("repeat_until_date", "Repeat until date must be in the future.")
        return cleaned_data

    def save(self, commit=True):
        instance = super(EventCreateForm, self).save(commit=False)
        instance.organisation_id = self.cleaned_data['organisation_id']
        instance.parent_event = instance
        if commit:
            instance.save()
        return instance
