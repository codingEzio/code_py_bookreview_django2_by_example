import os
from celery import Celery

# In case you might have multiple settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")

# Oh, do make sure you message broker is running!
# Either run 'rabbitmq-server' or 'redis-server' :)
app = Celery("myshop")

# 1. Find config in django.conf:settings (aka settings.py)
# 2. Related config needs to start with 'CELERY_' (e.g. BROKER_URL)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Searches packages for a “tasks.py” module (e.g. orders/tasks.py)
app.autodiscover_tasks()

# Keep Django & Message broker services running first!
# Commands (for more run 'celery --help')
# >> celery worker --app=myshop --loglevel=INFO
# >> celery flower --app=myshop --address=127.0.0.1 --port=10000
pass
