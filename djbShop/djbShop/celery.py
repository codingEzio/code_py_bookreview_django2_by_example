import os
from celery import Celery

# set environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djbShop.settings')

app = Celery(main='djbShop')

# all of the celery-related settings will be stored in 'settings.py'
# and each of them needs to start with 'CELERY_' (e.g. CELERY_BROKER_URL)
app.config_from_object(obj='django.conf:settings', namespace='CELERY')

# look for a 'task.py' file in each application dir
app.autodiscover_tasks()
