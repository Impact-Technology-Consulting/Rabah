import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rabah.settings")

from django.core.mail import send_mail
from django.conf import settings


subject = "Test Email"
body = "This is a test email sent using Django's send_mail and AWS SES."
recipient_email = (
    "dev.codertjay@gmail.com"  # Change this to your desired recipient email address
)

print(settings.EMAIL_PORT)
print(settings.EMAIL_HOST)
print(settings.EMAIL_USE_TLS)
print(settings.EMAIL_USE_SSL)
print(settings.EMAIL_HOST_PASSWORD)
print(settings.EMAIL_HOST_USER)
print(settings.DEFAULT_FROM_EMAIL)

sender_email = settings.EMAIL_HOST_USER

send_mail(subject, body, sender_email, [recipient_email], fail_silently=False)
