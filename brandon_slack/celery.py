import os
from celery import Celery

from brandon_slack import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandon_slack.settings')

app = Celery('brandon_slack')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
