from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = self.User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
            first_name="Admin",
            last_name="User",
            mobile=1234567890,
            verified=True,
            is_billing_verified=True,
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertEqual(superuser.first_name, "Admin")
        self.assertEqual(superuser.last_name, "User")
        self.assertEqual(superuser.mobile, 1234567890)
        self.assertTrue(superuser.verified)
        self.assertTrue(superuser.is_billing_verified)

    def test_create_user(self):
        """Test creating a normal user"""
        user = self.User.objects.create_user(
            email="user@example.com",
            password="userpassword",
            first_name="Normal",
            last_name="User",
            mobile=9876543210,
            verified=False,
            is_billing_verified=False,
        )
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.first_name, "Normal")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.mobile, 9876543210)
        self.assertFalse(user.verified)
        self.assertFalse(user.is_billing_verified)

    def test_update_user(self):
        """Test updating a user"""
        user = self.User.objects.create_user(
            email="user@example.com",
            password="userpassword",
            first_name="Normal",
            last_name="User",
        )
        new_first_name = "Updated"
        user.first_name = new_first_name
        user.save()
        self.assertEqual(user.first_name, new_first_name)

    def test_delete_user(self):
        """Test deleting a user"""
        user = self.User.objects.create_user(
            email="user@example.com",
            password="userpassword",
            first_name="Normal",
            last_name="User",
        )
        user.delete()
        self.assertFalse(self.User.objects.filter(email="user@example.com").exists())
