import random
import time
from datetime import datetime
from typing import Dict, List, Type, TypedDict

from celery import chunks, group
from celery.utils.log import get_task_logger
from hook_tasks.api_clients import hook_api_client
from hook_tasks.app import app
from hook_tasks.domains.sns_post.plurk.create_plurk import (
    create_new_release_plurk_by_release_feed,
)
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
from hook_tasks.infras.persistance.release_ticket.release_ticket_repository import (
    ReleaseTicketRepository,
)
from hook_tasks.on_demand.tasks import post_plurk
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


@app.task
def create_release_ticket_for_purpose(purpose: str) -> str:
    ticket_repo = ReleaseTicketRepository(hook_api_client)
    last_time = ticket_repo.get_last_ticket_created_time_with_purpose(purpose)
    ticket = ticket_repo.create_release_ticket_by_time_with_purpose(
        time=last_time, purpose=purpose
    )
    return ticket.id


@app.task
def post_new_releases_to_plurk(ticket_id: str) -> None:
    ticket_repo = ReleaseTicketRepository(hook_api_client)
    release_feeds = ticket_repo.get_release_feeds_by_ticket_id(ticket_id=ticket_id)

    for feed in release_feeds:
        plurk_model = create_new_release_plurk_by_release_feed(release_feed=feed)
        post_plurk.apply_async(args=(plurk_model.content, plurk_model.config.dict()))
        time.sleep(random.randint(5, 20))
