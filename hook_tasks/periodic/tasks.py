from typing import Dict, List, Type, TypedDict

from celery import group
from celery.utils.log import get_task_logger
from hook_tasks.app import app
from hook_tasks.domains.source_checksum.usecases.announcement_check import (
    AlterProductAnnouncementCheck,
    AmakuniProductAnnouncementCheck,
    GscProductAnnouncementCheck,
    NativeProductAnnouncementCheck,
    SiteSourceChceksum,
)
from hook_tasks.domains.spiders.usecases.scrapy_spider import (
    AlterProductAnnouncementSpiderUseCase,
    AmakuniProductAnnouncementSpiderUseCase,
    GscProductAnnouncementSpiderUseCase,
    NativeProductAnnouncementSpiderUseCase,
    ProductAnnouncementSpiderUseCase,
)
from requests import HTTPError

logger = get_task_logger(__name__)


class CheckSpider(TypedDict):
    check: Type[SiteSourceChceksum]
    spider: Type[ProductAnnouncementSpiderUseCase]


all_new_release_checks: Dict[str, CheckSpider] = {
    "alter": {
        "check": AlterProductAnnouncementCheck,
        "spider": AlterProductAnnouncementSpiderUseCase,
    },
    "gsc": {
        "check": GscProductAnnouncementCheck,
        "spider": GscProductAnnouncementSpiderUseCase,
    },
    "native": {
        "check": NativeProductAnnouncementCheck,
        "spider": NativeProductAnnouncementSpiderUseCase,
    },
    "amakuni": {
        "check": AmakuniProductAnnouncementCheck,
        "spider": AmakuniProductAnnouncementSpiderUseCase,
    },
}


@app.task
def check_new_release():
    check_groups = group(
        check_new_release_by_site_name.s(site_name=name)
        for name in all_new_release_checks.keys()
    )()
    check_groups.get(timeout=10)


@app.task(autoretry_for=(HTTPError,), retry_kwargs={"max_retries": 5})
def check_new_release_by_site_name(site_name: str) -> List[str]:
    spider_job_ids = []
    check_spider = all_new_release_checks.get(site_name)
    if check_spider:
        check = check_spider["check"]
        spider = check_spider["spider"]
        announcement_check = check.create()
        if announcement_check.is_changed():
            job_ids = spider.trigger()
            spider_job_ids.extend(job_ids)
        announcement_check.sync()
    return spider_job_ids
