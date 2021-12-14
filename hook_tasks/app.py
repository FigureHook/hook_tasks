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
    "push_discord_new_releases": {
        'task': 'hook_tasks.periodic.tasks.push_discord_new_releases',
        'schedule': crontab(minute='*/3')
    },
    "push_plurk_new_releases": {
        'task': 'hook_tasks.periodic.tasks.push_plurk_new_releases',
        'schedule': crontab(minute='*/10')
    },
    "check_new_release": {
        'task': 'hook_tasks.periodic.tasks.check_new_release',
        'schedule': crontab(minute='2, 12, 22 ,32, 42, 52, */5')
    }
}


if __name__ == '__main__':
    app.start()
