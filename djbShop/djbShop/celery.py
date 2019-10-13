import os
from celery import Celery

# Essential component to get Celery running
# - PROJ/__init__.py
# - PROJ/celery.py
# - APP/tasks.py

# Get celery running!
# 1. rabbitmq-server                        amaq
# 2. ./manage.py runserver                  well, try "complete an order, eh?"
# 3. celery -A PROJ_NAME worker -l info     run the worker & ready to process tasks
# 4. celery -A PROJ_NAME flower             web-based monitoring tool (optional)

# set environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djbShop.settings')

# When to use asynchronous tasks (examples)
# ~ time-consuming processes                        e.g. sending mail
# ~ processes that are subjected to conn failures   e.g. RETRY IT!
app = Celery(main='djbShop')

# all of the celery-related settings will be stored in 'settings.py'
# and each of them needs to start with 'CELERY_' (e.g. CELERY_BROKER_URL)
app.config_from_object(obj='django.conf:settings', namespace='CELERY')

# look for a 'task.py' file in each application dir
app.autodiscover_tasks()
