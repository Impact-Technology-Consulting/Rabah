import uuid

from django.db import models

from rabah_members.models import Member
from rabah_organisations.models import Organisation


# Create your models here.

class Event(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    group = models.ForeignKey
    name = models.CharField(max_length=250)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)


class EventMember(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    members_attendance = models.ManyToManyField("MemberAttendance", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


ATTENDANCE_STATUS = (
    ("PRESENT", "PRESENT"),
    ("ABSENT", "ABSENT"),
    ("LATE", "LATE"),
)


class MemberAttendance(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.CharField(max_length=250, choices=ATTENDANCE_STATUS)
    timestamp = models.DateTimeField(auto_now_add=True)
