import os
from typing import Type

from figure_hook.database import pgsql_session
from figure_hook.Tasks.periodic import (DiscordNewReleasePush,
                                        PlurkNewReleasePush)
from figure_hook.utils.announcement_checksum import (AlterChecksum,
                                                     GSCChecksum,
                                                     NativeChecksum,
                                                     SiteChecksum)

from figure_hook.utils.scrapyd_api import ScrapydUtil

from ..app import app


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
        result = news_push.execute()

    return result


@app.task
def check_new_release():
    scheduled_jobs = []
    site_checksums: list[Type[SiteChecksum]] = [
        AlterChecksum,
        GSCChecksum,
        NativeChecksum
    ]
    with pgsql_session():
        scrapy_util = ScrapydUtil(
            os.getenv("SCRAPYD_URL", "http://127.0.0.1:6800"), "product_crawler"
        )
        for site_checksum in site_checksums:
            checksum = site_checksum(scrapyd_util=scrapy_util)
            if checksum.is_changed:
                spider_jobs = checksum.trigger_crawler()
                scheduled_jobs.extend(spider_jobs)
                checksum.update()
    return scheduled_jobs
