import uuid

from django.db import models

from rabah_members.models import Member
from rabah_organisations.models import Organisation

# Create your models here.
REPEAT_CHOICES = (
    ("DAILY", "DAILY"),
    ("WEEKLY", "WEEKLY"),
    ("MONTHLY", "MONTHLY"),
    ("YEARLY", "YEARLY"),
)

REPEAT_END_CHOICES = (
    ("NEVER", "NEVER"),
    ("AFTER", "AFTER"),
    ("ON_DATE", "ON_DATE"),
)


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="events", blank=True)
    description = models.TextField()
    repeat = models.CharField(max_length=250, blank=True, null=True, choices=REPEAT_CHOICES)
    repeat_end = models.CharField(max_length=250, blank=True, null=True, choices=REPEAT_END_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    repeat_count = models.IntegerField(blank=True, null=True)
    repeat_until_date = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


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
