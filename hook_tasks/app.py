from celery import Celery
from celery.schedules import crontab

from hook_tasks.configs import get_celery_settings

from .helpers import JapanDatetimeHelper
from .periodic_canvas import gsc_aggresive_check

app = Celery("celery", config_source=get_celery_settings())
app.autodiscover_tasks(
    packages=[
        "hook_tasks.tasks.sns_post.discord",
        "hook_tasks.tasks.sns_post.plurk",
        "hook_tasks.tasks.new_release_check",
        "hook_tasks.tasks.common",
    ]
)


app.conf.beat_schedule = {
    "push_discord_new_releases": {
        "task": "hook_tasks.tasks.sns_post.discord.tasks.push_new_release_to_discord_webhook",
        "schedule": crontab(
            minute="*/10",
            hour="9-12,17-20",
            day_of_week="1-5",
            nowfun=JapanDatetimeHelper.now,
        ),
    },
    "push_plurk_new_releases": {
        "task": "hook_tasks.tasks.sns_post.plurk.tasks.post_new_releases_to_plurk",
        "schedule": crontab(
            minute="*/30",
            hour="11-13,18-20",
            day_of_week="1-5",
            nowfun=JapanDatetimeHelper.now,
        ),
    },
    "general_check_new_release": {
        "task": "hook_tasks.tasks.new_release_check.tasks.check_new_release",
        "schedule": crontab(
            minute="*/10",
            hour="9-13,16-20",
            day_of_week="1-5",
            nowfun=JapanDatetimeHelper.now,
        ),
    },
    "lead_gsc_daily_check": {
        "task": gsc_aggresive_check,
        "schedule": crontab(
            minute="59",
            hour="11",
            day_of_week="1-5",
            nowfun=JapanDatetimeHelper.now,
        ),
    },
    "additional_gsc_daily_check": {
        "task": gsc_aggresive_check,
        "schedule": crontab(
            minute="0,1,2,3",
            hour="12",
            day_of_week="1-5",
            nowfun=JapanDatetimeHelper.now,
        ),
    },
    # "check_delay": {
    #     "task": "hook_tasks.periodic.tasks.check_delay",
    #     "schedule": crontab(
    #         minute="0",
    #         hour="9-17",
    #         day_of_week="1-5",
    #         nowfun=JapanDatetimeHelper.now()
    #     ),
    # },
}
