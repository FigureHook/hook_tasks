import os
import sys

from celery import Celery
from celery.schedules import crontab

from hook_tasks import celeryconfig

sys.path.append(os.getcwd())

app = Celery("celery")

app.config_from_object(celeryconfig)
app.autodiscover_tasks(
    packages=[
        'hook_tasks.on_demand',
        'hook_tasks.periodic'
    ])

app.conf.beat_schedule = {
}


if __name__ == '__main__':
    app.start()
