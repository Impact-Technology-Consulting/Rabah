# Generated by Django 4.2.7 on 2024-03-11 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("first_name", models.CharField(max_length=150)),
                ("last_name", models.CharField(max_length=150)),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                ("mobile", models.IntegerField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("verified", models.BooleanField(default=False)),
                ("is_billing_verified", models.BooleanField(default=False)),
                ("date_joined", models.DateField(default=django.utils.timezone.now)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "profile_image",
                    models.ImageField(
                        default="profile_image.png", upload_to="profile_image"
                    ),
                ),
                ("career", models.CharField(blank=True, max_length=100, null=True)),
                ("about", models.TextField(blank=True, max_length=250, null=True)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("MALE", "MALE"), ("FEMALE", "FEMALE")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "marital_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("SINGLE", "Single"),
                            ("MARRIED", "Married"),
                            ("DIVORCED", "Divorced"),
                            ("SEPARATED", "Separated"),
                            ("WIDOWED", "Widowed"),
                            ("ANNULLED", "Annulled"),
                            ("DOMESTIC_PARTNERSHIP", "Domestic Partnership"),
                            ("CIVIL_UNION", "Civil Union"),
                            ("COMMON_LAW", "Common-Law Marriage"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=100, null=True)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
