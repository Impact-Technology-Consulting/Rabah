import uuid

from django.db import models
from django.db.models.signals import post_save

from rabah_organisations.models import Organisation, Group
from users.models import User


class MemberManager(models.Manager):
    def is_admin_user(self, user, organisation_id):
        member = self.filter(user=user, organisation_id=organisation_id).first()
        if not member:
            return False
        return member.is_admin_member


class Family(models.Model):
    name = models.CharField(max_length=250, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


FAMILY_RELATIONSHIP_CHOICES = [
    ("FATHER", "Father"),
    ("MOTHER", "Mother"),
    ("SISTER", "Sister"),
    ("BROTHER", "Brother"),
    ("SON", "Son"),
    ("DAUGHTER", "Daughter"),

]


class Member(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    is_admin_member = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # means they can access the organisation
    groups = models.ManyToManyField(Group, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, related_name='members')
    family_relationship = models.CharField(blank=True, null=True, max_length=250, choices=FAMILY_RELATIONSHIP_CHOICES)
    objects = MemberManager()

    def __str__(self):
        return f"{self.user.first_name} -- {self.user.last_name}"

    @property
    def get_family_members(self):
        if self.family:
            return self.family.members.all()
        return []

    def create_family(self):
        family = Family.objects.create(name=f"The {self.user.last_name} Family")
        self.family = family
        self.save()
        return


def post_save_create_member(sender, instance, *args, **kwargs):
    """
    This creates a  member once a organisation is being created
    :param instance:  the user created or updated
    """
    if instance:
        member = Member.objects.filter(organisation=instance, user=instance.owner).first()
        if not member:
            name = f"{instance.owner.last_name} Family"
            family = Family.objects.create(name=name)
            Member.objects.create(user=instance.owner, organisation=instance, is_admin_member=True, is_active=True,
                                  is_owner=True, family=family)


post_save.connect(post_save_create_member, sender=Organisation)
