import uuid
from datetime import datetime, timedelta

from django.db import models

from users.models import User


# Create your models here.

class Organisation(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    has_trial = models.BooleanField(default=False)  # this is used only for users who signed up with promo code
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class GroupManager(models.Manager):

    def calculate_group_increment_percentage(self, organisation_id):
        # Calculate the date of the last month
        last_month = datetime.now() - timedelta(days=30)

        # Count the number of groups since the last month
        current_month_count = Group.objects.filter(timestamp__gte=last_month, organisation_id=organisation_id).count()

        # Count the number of groups before the last month
        last_month_count = Group.objects.filter(timestamp__lt=last_month, organisation_id=organisation_id).count()

        # Calculate the percentage change
        if last_month_count == 0:
            return 100  # Handle the case where last month had no groups to avoid division by zero
        percentage_change = ((current_month_count - last_month_count) / last_month_count) * 100

        return percentage_change


class Group(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='group_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = GroupManager()

    class Meta:
        ordering = ["-timestamp"]

    def members(self):
        return self.member_set.all()

    def random_10_members(self):
        return self.member_set.all().order_by('?')[:10]

    def random_10_admin_members(self):
        return self.member_set.filter(is_admin_member=True).order_by('?')[:10]

    def members_count(self):
        return self.member_set.all().count()

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def group_owner(self):
        admin_member = self.member_set.filter(is_owner=True).order_by('timestamp').first()
        if admin_member:
            return admin_member
        return None

    def __str__(self):
        return self.name
