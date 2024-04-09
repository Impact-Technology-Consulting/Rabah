from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime, timedelta
from .models import Organisation, Group


class OrganisationModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )

    def test_create_organisation(self):
        organisation = Organisation.objects.create(
            owner=self.user, name="Test Organisation", has_trial=True
        )
        self.assertEqual(organisation.owner, self.user)
        self.assertEqual(organisation.name, "Test Organisation")
        self.assertTrue(organisation.has_trial)
        self.assertTrue(organisation.timestamp)

    def test_create_organisation_without_owner(self):
        organisation = Organisation.objects.create(
            name="Test Organisation", has_trial=True
        )
        self.assertIsNone(organisation.owner)
        self.assertEqual(organisation.name, "Test Organisation")
        self.assertTrue(organisation.has_trial)
        self.assertTrue(organisation.timestamp)


class GroupModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.organisation = Organisation.objects.create(
            owner=self.user, name="Test Organisation", has_trial=True
        )

    def test_create_group(self):
        group = Group.objects.create(
            organisation=self.organisation,
            name="Test Group",
            description="Test description",
        )
        self.assertEqual(group.organisation, self.organisation)
        self.assertEqual(group.name, "Test Group")
        self.assertEqual(group.description, "Test description")
        self.assertTrue(group.timestamp)

    def test_group_owner(self):
        group = Group.objects.create(
            organisation=self.organisation,
            name="Test Group",
            description="Test description",
        )
        self.assertIsNone(group.group_owner())

        # Make user the owner
        group_member = group.member_set.create(
            user=self.user, is_owner=True, is_admin_member=True, is_active=True
        )
        self.assertEqual(group.group_owner(), group_member)
