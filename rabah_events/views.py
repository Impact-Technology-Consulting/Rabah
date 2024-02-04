import json

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from rabah_events.forms import EventCreateForm, EventUpdateForm
from rabah_events.models import Event, EventMember, MemberAttendance
from rabah_events.tasks import create_event_for_repeat_count, create_event_for_until_date
from rabah_members.models import Member
from rabah_members.utils import query_members
from users.mixin import AuthAndAdminOrganizationMemberMixin


class EventView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is the calendar page where users get access to view events using the calendar
    """

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
            event = form.save()

            #  create the event for the automation
            if event.repeat_end == "AFTER":
                create_event_for_repeat_count(event.id)
            elif event.repeat_end == "ON_DATE":
                create_event_for_until_date(event.id)

            messages.success(self.request, "Successfully create event")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            for error in form.errors:
                messages.warning(request, f"{error}: {form.errors[error][0]}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class EventUpdateView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to update an event
    """

    def get(self, request, event_id):
        event = Event.objects.filter(id=event_id, organisation_id=self.organisation_id).first()
        if not event:
            messages.error(request, "Event with this id does not exist in this organisation")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        form = EventUpdateForm(self.organisation_id, instance=event)
        context = {
            "form": form,
            "event": event
        }
        return render(request, "dashboard/event_update.html", context)

    def post(self, request, event_id):
        event = Event.objects.filter(id=event_id, organisation_id=self.organisation_id).first()
        if not event:
            messages.error(request, "Event with this id does not exist in this organisation")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        form = EventUpdateForm(self.organisation_id, data=request.POST, files=request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, "Event updated successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            for error in form.errors:
                messages.warning(request, f"{error}: {form.errors[error][0]}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class EventListView(AuthAndAdminOrganizationMemberMixin, ListView):
    """
    this is used to list all the events available, and it only shows from future events or current events
    """
    queryset = Event.objects.all()
    template_name = "dashboard/event_list.html"
    context_object_name = "events"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(organisation_id=self.organisation_id, start_date__gte=timezone.now())


class EventCalendarView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to get all the calendar info api  on the events available
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
        search = request.GET.get("search")
        status = request.GET.get("status")

        event = Event.objects.filter(id=event_id, organisation_id=self.organisation_id).first()
        if not event:
            messages.error(request, "Event with this id does not exist in this organisation")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        members = Member.objects.filter(organisation_id=self.organisation_id)

        if search:
            members = query_members(search, members)

        member_attendance = MemberAttendance.objects.filter(event_id=event_id, organisation_id=self.organisation_id)

        if status == "PRESENT":
            # Get a list of member IDs with status "PRESENT"
            present_member_ids = member_attendance.filter(status="PRESENT").values_list("member_id", flat=True)
            # Filter members using the list of IDs
            members = members.filter(id__in=present_member_ids)

        elif status == "ABSENT":
            # Get a list of member IDs with status "PRESENT"
            present_member_ids = member_attendance.filter(status="PRESENT").values_list("member_id", flat=True)
            # Exclude members with the list of IDs
            members = members.exclude(id__in=present_member_ids)

        present_count = member_attendance.filter(status="PRESENT").count()
        absent_count = Member.objects.filter(organisation_id=self.organisation_id).count() - present_count

        context = {
            "members": members,
            "event": event,
            "present_count":present_count,
            "absent_count":absent_count
        }
        return render(request, "dashboard/mark_attendance.html", context)


class MarkMultipleMemberAttendanceView(AuthAndAdminOrganizationMemberMixin, View):
    """
    this is used to update or create a member attendance it can mark multiple users at once
    """

    def post(self, request, event_id):
        data = json.loads(request.body)
        members_ids = data.get("checkedCheckboxes")
        if not members_ids:
            return JsonResponse({"message": "No members selected"}, status=400)
        event = Event.objects.filter(id=event_id, organisation_id=self.organisation_id).first()
        if not event:
            messages.error(request, "Event with this id does not exist in this organisation")
            return JsonResponse({"message": "No event "}, status=404)
        event_member, created = EventMember.objects.get_or_create(event=event, organisation=event.organisation)

        for member_id in members_ids:
            member = Member.objects.filter(id=member_id.get("id"), organisation_id=self.organisation_id).first()
            if not member:
                return JsonResponse({"message": "Member with this id does not exist in this organisation"},
                                    status=400)
            # create the member attendance or get it
            member_attendance = MemberAttendance.objects.filter(member=member,
                                                                organisation=event.organisation,
                                                                event=event).first()
            if not member_attendance:
                member_attendance = MemberAttendance.objects.create(member=member,
                                                                    organisation=event.organisation,
                                                                    event=event)
            if member_id.get("is_checked"):
                member_attendance.status = "PRESENT"
                member_attendance.save()
                event_member.members_attendance.add(member_attendance)
                return JsonResponse({"message": "Attendance marked successfully for PRESENT"}, status=200)
            else:
                member_attendance.status = "ABSENT"
                member_attendance.save()
                event_member.members_attendance.add(member_attendance)
                return JsonResponse({"message": "Attendance marked successfully for ABSENT"}, status=200)
