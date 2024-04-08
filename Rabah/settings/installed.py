INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
EXTERNAL_INSTALLED_APPS = [
    #  for authentications
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "crispy_forms",
    "allauth.socialaccount.providers.google",
    # for running tasks
    "django_celery_beat",
    # google captcha
    "django_recaptcha",
]

LOCAL_INSTALLED_APPS = [
    "users",
    "rabah_subscriptions",
    "rabah_organisations",
    "rabah_members",
    "rabah_home_pages",
    "rabah_events",
    "rabah_dashboard",
    "rabah_contributions",
    "rabah_communications",
]
INSTALLED_APPS += EXTERNAL_INSTALLED_APPS
INSTALLED_APPS += LOCAL_INSTALLED_APPS
