import uuid
from datetime import datetime, timedelta

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
    ("AFTER", "AFTER"),
    ("ON_DATE", "ON_DATE"),
)


class EventManager(models.Manager):
    def calculate_event_increment_percentage(self, organisation_id):
        # Calculate the date of the last month
        last_month = datetime.now() - timedelta(days=30)

        # Count the number of events since the last month
        current_month_count = Event.objects.filter(timestamp__gte=last_month, organisation_id=organisation_id).count()

        # Count the number of events before the last month
        last_month_count = Event.objects.filter(timestamp__lt=last_month, organisation_id=organisation_id).count()

        # Calculate the percentage change
        if last_month_count == 0:
            return 100  # Handle the case where last month had no events to avoid division by zero
        percentage_change = ((current_month_count - last_month_count) / last_month_count) * 100

        return percentage_change


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
    repeat_until_date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    #  for event that could have repeat count, or repeat until date
    parent_event = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    objects = EventManager()

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
