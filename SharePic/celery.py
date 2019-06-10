from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
env = os.environ.get("PY3_DJANGO2_SETTING_ENV", "develop")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SharePic.%s' % env)

app = Celery('share_pic')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

import time


@app.task(bind=True)
def debug_task(self):
    time.sleep(5)
    print('Request: {0!r}'.format(self.request))


from celery import shared_task


@shared_task
def ttt():
    print("xxxxxxxxxxxxxxxxxxxxxxxxxx")
    return "yyyyyyyyyyyyyyyyyyyyyy"
