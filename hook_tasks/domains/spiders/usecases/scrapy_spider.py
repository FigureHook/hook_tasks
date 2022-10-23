from typing import List

from hook_tasks.config import SpiderSettings
from scrapyd_client.lib import get_spiders, schedule

from ..spider_config import EmptyConfig, SpiderConfig

__all__ = ("get_spiders_from_project", "trigger_spider")


def get_spiders_from_project(
    project_name: str, spider_name_pattern: str = "*"
) -> List[str]:
    spiders = get_spiders(
        url=SpiderSettings.SCRAPY_URL, project=project_name, pattern=spider_name_pattern
    )
    return spiders


def trigger_spider(
    project_name: str, spider_name: str, config: SpiderConfig = EmptyConfig()
) -> str:
    job_id = schedule(
        url=SpiderSettings.SCRAPY_URL,
        project=project_name,
        spider=spider_name,
        args=config.asdict(),
    )
    return job_id
