from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from rabah_events.forms import EventCreateForm
from rabah_events.models import Event, EventMember, MemberAttendance
from rabah_members.models import Member
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
        form = EventCreateForm(organisation_id, data=self.request.POST, files=self.request.FILES)
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


class MarkAttendancePageView(AuthAndAdminOrganizationMemberMixin, View):

    def get(self, request, event_id):
        event = Event.objects.filter(id=event_id, organisation_id=self.organisation_id).first()
        if not event:
            messages.error(request, "Event with this id does not exist in this organisation")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        members = Member.objects.filter(organisation_id=self.organisation_id)
        context = {
            "members": members,
            "event": event
        }
        return render(request, "dashboard/mark_attendance.html", context)


class UpdateOrCreateMemberAttendanceView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to update or create a member attendance
    """

    def post(self, request):
        event_id = request.POST.get("event_id")
        member_id = request.POST.get("member_id")
        attendance = request.POST.get("attendance")
        event = Event.objects.filter(id=event_id, organisation_id=self.organisation_id).first()
        if not event:
            messages.error(request, "Event with this id does not exist in this organisation")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        member = Member.objects.filter(id=member_id, organisation_id=self.organisation_id).first()
        if not member:
            return JsonResponse({"message": "Member with this id does not exist in this organisation"}, status=400)
        event_member, created = EventMember.objects.get_or_create(event=event, organisation=event.organisation)

        # create the member attendance or get it
        member_attendance, created = MemberAttendance.objects.get_or_create(member=member,
                                                                            organisation=event.organisation,
                                                                            event=event)
        member_attendance.status = f"{attendance}".upper()
        member_attendance.save()

        event_member.members_attendance.add(member_attendance)
        member_attendance.save()

        return JsonResponse({"message": "Attendance marked successfully"}, status=200)
