from typing import Dict, Type

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


all_product_announcement_checks: Dict[
    Type[SiteSourceChceksum], Type[ProductAnnouncementSpiderUseCase]
] = {
    AlterProductAnnouncementCheck: AlterProductAnnouncementSpiderUseCase,
    GscProductAnnouncementCheck: GscProductAnnouncementSpiderUseCase,
    NativeProductAnnouncementCheck: NativeProductAnnouncementSpiderUseCase,
    AmakuniProductAnnouncementCheck: AmakuniProductAnnouncementSpiderUseCase,
}


@app.task
def check_new_release():
    scheduled_jobs = []
    for check, product_spider in all_product_announcement_checks.items():
        announcement_check = check.create()
        try:
            if announcement_check.is_changed():
                job_id = product_spider.trigger()
                scheduled_jobs.append(job_id)
            announcement_check.sync()
        except HTTPError:
            msg = f"Failed to extract feature from {check.__source_site__}."
            logger.error(msg)

    return scheduled_jobs
