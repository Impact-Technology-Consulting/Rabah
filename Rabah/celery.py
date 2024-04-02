import os

from celery import Celery
from celery.schedules import crontab
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rabah.settings")

# used redis for saving task and running task
app = Celery(
    "Rabah", broker=config("CELERY_BROKER_URL"), backend=config("CELERY_BROKER_URL")
)
app.config_from_object("django.conf:settings")

# Load task modules from all registered Django app configs.
app.conf.broker_url = config("CELERY_BROKER_URL")

#  this is used to make an automation either send mail during a specific time
#  or delete some stuff or more
app.conf.beat_schedule = {
    #  This is used to check inactive subscription every 23 hours
    "check_and_cancel_inactive_subscription": {
        "task": "rabah_subscriptions.tasks.check_and_cancel_inactive_subscription",
        "schedule": crontab(hour=23),
    }
}


@app.task
def debug_task():
    print(f"Request: ")
