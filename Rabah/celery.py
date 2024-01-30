import os

from celery import Celery
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rabah.settings')

# used redis for saving task and running task
app = Celery('Rabah', broker=config("CELERY_BROKER_URL"), backend=config("CELERY_BROKER_URL"))
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.conf.broker_url = config("CELERY_BROKER_URL")

#  this is used to make an automation either send mail during a specific time
#  or delete some stuff or more
app.conf.beat_schedule = {

}


@app.task
def debug_task():
    print(f'Request: ')
