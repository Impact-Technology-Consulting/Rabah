from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile
from users.forms import (
    RabahSignupForm,
    RabahLoginForm,
    UserProfileUpdateForm,
    ChangePasswordForm,
)


class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "user@example.com",
            "password": "userpassword",
            "first_name": "John",
            "last_name": "Doe",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_create_user(self):
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertTrue(self.user.check_password(self.user_data["password"]))
        self.assertEqual(self.user.first_name, self.user_data["first_name"])
        self.assertEqual(self.user.last_name, self.user_data["last_name"])
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(**self.user_data)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "John",
            "last_name": "Doe",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.profile_data = {
            "user": self.user,
            "career": "Software Engineer",
            "about": "A brief description",
            "gender": "MALE",
            "marital_status": "SINGLE",
            "address": "123 Main St",
            "date_of_birth": "1990-01-01",
        }
        self.user_profile = UserProfile.objects.create(**self.profile_data)

    def test_create_user_profile(self):
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.career, self.profile_data["career"])
        self.assertEqual(self.user_profile.about, self.profile_data["about"])
        self.assertEqual(self.user_profile.gender, self.profile_data["gender"])
        self.assertEqual(
            self.user_profile.marital_status, self.profile_data["marital_status"]
        )
        self.assertEqual(self.user_profile.address, self.profile_data["address"])
        self.assertEqual(
            str(self.user_profile.date_of_birth), self.profile_data["date_of_birth"]
        )


class RabahSignupFormTest(TestCase):
    def test_signup_form_valid(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "organisation_name": "Company",
            "email": "john.doe@example.com",
            "password1": "securepassword",
            "password2": "securepassword",
        }
        form = RabahSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        # Test with invalid data to ensure form validation works
        form_data = {
            "first_name": "John",
            "last_name": "",  # Last name is required
            "organisation_name": "Company",
            "email": "invalid-email",  # Invalid email format
            "password1": "password",
            "password2": "differentpassword",
        }
        form = RabahSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)


class RabahLoginFormTest(TestCase):
    def test_login_form_valid(self):
        form_data = {
            "email": "john.doe@example.com",
            "password": "securepassword",
        }
        form = RabahLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        # Test with invalid data to ensure form validation works
        form_data = {
            "email": "invalid-email",  # Invalid email format
            "password": "",  # Password not provided
        }
        form = RabahLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("password", form.errors)


class UserProfileUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john.doe@example.com",
            email="john.doe@example.com",
            password="securepassword",
            first_name="John",
            last_name="Doe",
        )
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_user_profile_update_form_valid(self):
        form_data = {
            "first_name": "UpdatedJohn",
            "last_name": "UpdatedDoe",
            "email": "john.doe@example.com",  # Same email should be valid
            "mobile": "123456789",
            "date_of_birth": "1990-01-01",
            "profile_image": SimpleUploadedFile("profile.jpg", b"file_content"),
            # Add other required fields based on your form
        }
        form = UserProfileUpdateForm(data=form_data, instance=self.user_profile)
        self.assertTrue(form.is_valid())

    def test_user_profile_update_form_invalid(self):
        # Test with invalid data to ensure form validation works
        form_data = {
            "first_name": "",
            "last_name": "UpdatedDoe",
            "email": "john.doe@example.com",  # Same email should be valid
            "mobile": "invalid-mobile",  # Invalid mobile format
            "date_of_birth": "invalid-date",  # Invalid date format
            "profile_image": SimpleUploadedFile("profile.jpg", b"file_content"),
        }
        form = UserProfileUpdateForm(data=form_data, instance=self.user_profile)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)
        self.assertIn("mobile", form.errors)


class ChangePasswordFormTest(TestCase):
    def test_change_password_form_valid(self):
        form_data = {
            "password": "newsecurepassword",
            "confirm_password": "newsecurepassword",
        }
        form = ChangePasswordForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_change_password_form_invalid(self):
        # Test with invalid data to ensure form validation works
        form_data = {
            "password": "newsecurepassword",
            "confirm_password": "differentpassword",
        }
        form = ChangePasswordForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("confirm_password", form.errors)

