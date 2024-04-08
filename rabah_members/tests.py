from django.test import TestCase
from django.utils import timezone
from .models import Family, Member
from datetime import datetime, timedelta
from users.models import User
from rabah_organisations.models import Organisation, Group


class FamilyModelTests(TestCase):
    def test_create_family(self):
        """Test creating a family"""
        timestamp = timezone.now()
        family = Family.objects.create(name="Smith Family", timestamp=timestamp)

        self.assertEqual(family.name, "Smith Family")
        self.assertEqual(family.timestamp, timestamp)

    def test_update_family(self):
        """Test updating a family"""
        timestamp = timezone.now()
        family = Family.objects.create(name="Smith Family", timestamp=timestamp)
        new_family_name = "Jones Family"
        family.name = new_family_name
        family.save()

        self.assertEqual(family.name, new_family_name)

    def test_delete_family(self):
        """Test deleting a family"""
        timestamp = timezone.now()
        family = Family.objects.create(name="Smith Family", timestamp=timestamp)
        family.delete()

        self.assertFalse(Family.objects.filter(name="Smith Family").exists())


class MemberModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="user@example.com",
            password="password",
            first_name="John",
            last_name="Doe",
        )
        self.organisation = Organisation.objects.create(name="Test Organisation")
        self.family = Family.objects.create(name="Doe Family")

    def test_create_member(self):
        """Test creating a member"""
        timestamp = timezone.now()
        member = Member.objects.create(
            user=self.user,
            organisation=self.organisation,
            is_owner=True,
            is_admin_member=True,
            is_active=True,
            timestamp=timestamp,
            family=self.family,
            family_relationship="Father",
        )

        self.assertEqual(member.user, self.user)
        self.assertEqual(member.organisation, self.organisation)
        self.assertTrue(member.is_owner)
        self.assertTrue(member.is_admin_member)
        self.assertTrue(member.is_active)
        self.assertEqual(member.timestamp, timestamp)
        self.assertEqual(member.family, self.family)
        self.assertEqual(member.family_relationship, "Father")

    def test_update_member(self):
        """Test updating a member"""
        timestamp = timezone.now()
        member = Member.objects.create(
            user=self.user,
            organisation=self.organisation,
            is_owner=False,
            is_admin_member=False,
            is_active=False,
            timestamp=timestamp,
            family=self.family,
            family_relationship="Mother",
        )

        new_first_name = "Jane"
        self.user.first_name = new_first_name
        self.user.save()

        self.assertEqual(member.user.first_name, new_first_name)

    def test_delete_member(self):
        """Test deleting a member"""
        timestamp = timezone.now()
        member = Member.objects.create(
            user=self.user,
            organisation=self.organisation,
            is_owner=False,
            is_admin_member=False,
            is_active=False,
            timestamp=timestamp,
            family=self.family,
            family_relationship="Brother",
        )

        member.delete()

        self.assertFalse(Member.objects.filter(user=self.user).exists())
