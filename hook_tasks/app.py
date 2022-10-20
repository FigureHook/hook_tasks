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

# app.conf.beat_schedule = {
#     "push_discord_new_releases": {
#         'task': 'hook_tasks.periodic.tasks.push_discord_new_releases',
#         'schedule': crontab(
#             minute='*/10',
#             hour='9-17',
#             day_of_week='1-5',
#         )
#     },
#     "push_plurk_new_releases": {
#         'task': 'hook_tasks.periodic.tasks.push_plurk_new_releases',
#         'schedule': crontab(
#             minute='1, 3, 13, 23 ,33, 43, 53',
#             hour='9-17',
#             day_of_week='1-5',
#         )
#     },
#     "check_new_release": {
#         'task': 'hook_tasks.periodic.tasks.check_new_release',
#         'schedule': crontab(
#             minute='0, 2, 12, 22 ,32, 42, 52',
#             hour='9-17',
#             day_of_week='1-5',
#         )
#     },
#     "check_delay": {
#         'task': 'hook_tasks.periodic.tasks.check_delay',
#         'schedule': crontab(
#             minute='0',
#             hour='9-17',
#             day_of_week='1-5',
#         )
#     }
# }

