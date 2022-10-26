from typing import Dict, Type

from hook_tasks.app import app
from hook_tasks.domains.source_checksum.usecases.announcement_check import (
    AlterProductAnnouncementCheck, AmakuniProductAnnouncementCheck,
    GscProductAnnouncementCheck, NativeProductAnnouncementCheck,
    SiteSourceChceksum)
from hook_tasks.domains.spiders.usecases.scrapy_spider import (
    AlterProductAnnouncementSpiderUseCase, GscProductAnnouncementSpiderUseCase,
    NativeProductAnnouncementSpiderUseCase, ProductAnnouncementSpiderUseCase,
    trigger_spider)

all_checks: Dict[Type[SiteSourceChceksum], Type[ProductAnnouncementSpiderUseCase]] = {
    AlterProductAnnouncementCheck: AlterProductAnnouncementSpiderUseCase,
    GscProductAnnouncementCheck: GscProductAnnouncementSpiderUseCase,
    NativeProductAnnouncementCheck: NativeProductAnnouncementSpiderUseCase,
}


@app.task
def check_new_release():
    scheduled_jobs = []
    for check, product_spider in all_checks.items():
        announcement_check = check.create()
        if announcement_check.is_changed():
            job_id = product_spider.trigger()
            scheduled_jobs.append(job_id)
        announcement_check.sync()

    return scheduled_jobs
