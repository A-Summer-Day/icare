from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icare.settings')

# create a Celery instance and configure it using the settings from Django.
app = Celery('icare')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Configure Celery Beat
app.conf.beat_schedule = {
    'send-email-task': {
        'task': 'myhealth.tasks.send_email_task',  
        'schedule': crontab(minute = 0, hour = 12), 
    },
}