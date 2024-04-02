import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

print("Using production")

DEBUG = False
SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = ["rabah360.com", "www.rabah360.com"]

#  read more https://docs.djangoproject.com/en/4.1/ref/middleware/#http-strict-transport-security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600  # one hour
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
#  I JUST ONLY SET THE DATABASE FOR POSTGRES, BUT IT COULD BE MODIFIED
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("POSTGRES_DB", default=""),
        "USER": config("POSTGRES_USER", default=""),
        "PASSWORD": config("POSTGRES_PASSWORD", default=""),
        "HOST": config("POSTGRES_HOST", default=""),
        "PORT": config("POSTGRES_PORT", default=""),
    }
}

sentry_sdk.init(
    dsn=config("SENTRY_URL"),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

STRIPE_PUBLIC_KEY = config("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
