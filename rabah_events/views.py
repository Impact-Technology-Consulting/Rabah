from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from rabah_events.forms import EventCreateForm
from rabah_events.models import Event
from users.mixin import AuthAndAdminOrganizationMemberMixin


class EventView(AuthAndAdminOrganizationMemberMixin, View):

    def get(self, request):
        organisation_id = self.organisation_id
        form = EventCreateForm(organisation_id)

        # Get all events for the organization
        events = Event.objects.filter(organisation_id=organisation_id)

        # Filter today's events based on the start_date
        todays_events = events.filter(start_date__date=timezone.now().date())

        context = {
            "form": form,
            "events": events,
            "todays_events": todays_events,
        }
        return render(request, "dashboard/event.html", context)

    def post(self, request):
        organisation_id = self.organisation_id
        form = EventCreateForm(organisation_id, data=self.request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Successfully create event")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Error creating event")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class EventCalendarView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to get all the calendar info on the events available
    """

    def get(self, request):
        organisation_id = self.organisation_id

        events = Event.objects.filter(organisation_id=organisation_id)
        data = []
        for event in events:
            data.append({
                'id': event.id,
                'title': event.name,
                'start': event.start_date.isoformat(),
                'end': event.end_date.isoformat(),
            })
        return JsonResponse(data, safe=False)


class EventDeleteView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to delete an event
    """

    def get(self, request, event_id):
        event = Event.objects.filter(id=event_id, organisation_id=self.organisation_id).first()
        if not event:
            messages.error(request, "Event with this id does not exist in this organisation")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        event.delete()
        messages.success(request, "Event deleted successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
