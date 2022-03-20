import os
from typing import Type

from celery.utils.log import get_task_logger
from figure_hook.database import pgsql_session
from figure_hook.Tasks.periodic import (DiscordNewReleasePush,
                                        PlurkNewReleasePush)
from figure_hook.SourceChecksum.product_announcement_checksum import (AlterProductAnnouncementChecksum,
                                                                      GSCProductAnnouncementChecksum,
                                                                      NativeProductAnnouncementChecksum)
from figure_hook.SourceChecksum.abcs import ProductAnnouncementChecksum
from figure_hook.utils.scrapyd_api import ScrapydUtil
from requests.exceptions import HTTPError

from ..app import app

logger = get_task_logger(__name__)


@app.task
def push_discord_new_releases():
    with pgsql_session() as session:
        news_push = DiscordNewReleasePush(session=session)
        result = news_push.execute()

    return result


@app.task
def push_plurk_new_releases():
    with pgsql_session() as session:
        news_push = PlurkNewReleasePush(session=session)
        result = news_push.execute(logger=logger)

    return result


@app.task
def check_new_release():
    scheduled_jobs = []
    site_checksums: list[Type[ProductAnnouncementChecksum]] = [
        AlterProductAnnouncementChecksum,
        GSCProductAnnouncementChecksum,
        NativeProductAnnouncementChecksum
    ]
    with pgsql_session():
        scrapy_util = ScrapydUtil(
            os.getenv("SCRAPYD_URL", "http://127.0.0.1:6800"), "product_crawler"
        )
        for site_checksum in site_checksums:
            try:
                checksum = site_checksum(scrapyd_util=scrapy_util)
                if checksum.is_changed:
                    spider_jobs = checksum.trigger_crawler()
                    checksum.__spider__
                    scheduled_jobs.append({
                        checksum.__spider__: spider_jobs
                    })
                    checksum.update()
            except HTTPError as err:
                scheduled_jobs.append({
                    site_checksum.__spider__: err
                })

    return scheduled_jobs
