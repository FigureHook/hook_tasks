from abc import ABC
from typing import ClassVar, List

from figure_parser.enums import AlterCategory, GSCCategory, NativeCategory
from hook_tasks.configs import SpiderSettings
from hook_tasks.helpers import JapanDatetimeHelper
from scrapyd_client.lib import get_spiders, schedule

from ..spider_config import (
    AlterProductSpiderConfig,
    EmptyConfig,
    GscProductSpiderConfig,
    NativeProductSpiderConfig,
    AmakuniProductSpiderConfig,
    SpiderConfig,
)

__all__ = ("get_spiders_from_project", "trigger_spider")

spider_seetings = SpiderSettings()  # type: ignore


def get_spiders_from_project(
    project_name: str, spider_name_pattern: str = "*"
) -> List[str]:
    spiders = get_spiders(
        url=spider_seetings.SCRAPY_URL,
        project=project_name,
        pattern=spider_name_pattern,
    )
    return spiders


def trigger_spider(
    project_name: str, spider_name: str, config: SpiderConfig = EmptyConfig()
) -> str:
    job_id = schedule(
        url=spider_seetings.SCRAPY_URL,
        project=project_name,
        spider=spider_name,
        args=config.asdict(),
    )
    return job_id


class ProductAnnouncementSpiderUseCase(ABC):
    project: ClassVar[str] = "product_crawler"

    spider: ClassVar[str]
    spider_configs: ClassVar[List[SpiderConfig]]

    @classmethod
    def trigger(cls) -> List[str]:
        job_ids: List[str] = []
        for config in cls.spider_configs:
            job_id = trigger_spider(
                project_name=cls.project, spider_name=cls.spider, config=config
            )
            job_ids.append(job_id)
        return job_ids


class GscProductAnnouncementSpiderUseCase(ProductAnnouncementSpiderUseCase):
    spider: ClassVar[str] = "gsc_product"
    spider_configs: ClassVar[List[SpiderConfig]] = [
        GscProductSpiderConfig(
            begin_year=JapanDatetimeHelper.today().year,
            end_year=JapanDatetimeHelper.today().year,
            category=GSCCategory.SCALE,
            is_announcement_spider=True,
        )
    ]


class AlterProductAnnouncementSpiderUseCase(ProductAnnouncementSpiderUseCase):
    spider: ClassVar[str] = "alter_product"
    spider_configs: ClassVar[List[SpiderConfig]] = [
        AlterProductSpiderConfig(
            begin_year=JapanDatetimeHelper.today().year,
            category=AlterCategory.FIGURE,
            is_announcement_spider=True,
        ),
        AlterProductSpiderConfig(
            begin_year=JapanDatetimeHelper.today().year,
            category=AlterCategory.ALTAIR,
            is_announcement_spider=True,
        ),
        AlterProductSpiderConfig(
            begin_year=JapanDatetimeHelper.today().year,
            category=AlterCategory.COLLABO,
            is_announcement_spider=True,
        ),
    ]


class NativeProductAnnouncementSpiderUseCase(ProductAnnouncementSpiderUseCase):
    spider: ClassVar[str] = "native_product"
    spider_configs: ClassVar[List[SpiderConfig]] = [
        NativeProductSpiderConfig(
            end_page=1, category=NativeCategory.CHARACTERS, is_announcement_spider=True
        ),
        NativeProductSpiderConfig(
            end_page=1, category=NativeCategory.CREATORS, is_announcement_spider=True
        ),
    ]


class AmakuniProductAnnouncementSpiderUseCase(ProductAnnouncementSpiderUseCase):
    spider: ClassVar[str] = "amakuni_product"
    spider_configs: ClassVar[List[SpiderConfig]] = [
        AmakuniProductSpiderConfig(
            is_announcement_spider=True, begin_year=JapanDatetimeHelper.today().year
        )
    ]
