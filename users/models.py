import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.signing import TimestampSigner
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

GENDER_CHOICES = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
)
MEMBERSHIP_PERMISSIONS = (
    ("ADMIN", "ADMIN"),
    ("MEMBER", "MEMBER"),
)
MARITAL_STATUS_CHOICES = (
    ("SINGLE", "Single"),
    ("MARRIED", "Married"),
    ("DIVORCED", "Divorced"),
    ("SEPARATED", "Separated"),
    ("WIDOWED", "Widowed"),
    ("ANNULLED", "Annulled"),
    ("DOMESTIC_PARTNERSHIP", "Domestic Partnership"),
    ("CIVIL_UNION", "Civil Union"),
    ("COMMON_LAW", "Common-Law Marriage"),
)


class UserManager(BaseUserManager):
    """
    This is used to add extra queryset or add more functionality to the user models
    by creating helper functions
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
     user models  inheriting from AbstractBaseUser to add extra fields
     and PermissionsMixin to add permission
    I actually added blank and null in some fields
    the username field is converted to use the email field
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    # this tells django the username field because sometimes you can change it to email or username itself
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(_("email address"), unique=True,blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    is_billing_verified = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def generate_token(self):
        signer = TimestampSigner()
        token = signer.sign(str(self.id))

        return token

    @staticmethod
    def verify_token(token, max_age=86400):  # 1 day expiration by default
        signer = TimestampSigner()
        try:
            user_id = signer.unsign(token, max_age=max_age)

            return User.objects.get(id=user_id)
        except (
            Exception
        ) as a:  # (BadSignature, SignatureExpired, ValueError, User.DoesNotExist):
            print(a)
            return None


# Create your models here.
class UserProfile(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_profile",
    )
    profile_image = models.ImageField(
        upload_to="profile_image", default="profile_image.png"
    )
    career = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(max_length=250, blank=True, null=True)
    gender = models.CharField(
        max_length=10, blank=True, null=True, choices=GENDER_CHOICES
    )
    marital_status = models.CharField(
        max_length=50, blank=True, null=True, choices=MARITAL_STATUS_CHOICES
    )
    address = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def profileImageURL(self):
        try:
            profile_image = self.profile_image.url
        except:
            profile_image = None
        return profile_image


def post_save_create_user_profile(sender, instance, *args, **kwargs):
    """
    This creates a user  profile once a user is being created
    :param instance:  the user created or updated
    """
    if instance:
        user_profile = UserProfile.objects.filter(user=instance).first()
        if not user_profile:
            UserProfile.objects.create(user=instance)


post_save.connect(post_save_create_user_profile, sender=User)
