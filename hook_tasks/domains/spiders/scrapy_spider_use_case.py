from abc import ABC, abstractmethod
from typing import ClassVar, List

from figure_parser.enums import AlterCategory, GSCCategory, NativeCategory
from scrapyd_client.lib import get_spiders, schedule

from hook_tasks.configs import SpiderSettings
from hook_tasks.helpers import JapanDatetimeHelper

from .value_objects.spider_config import (
    AlterProductSpiderConfig,
    AmakuniProductSpiderConfig,
    EmptyConfig,
    GscProductSpiderConfig,
    NativeProductSpiderConfig,
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


class ProductAnnouncementSpider(ABC):
    project: ClassVar[str] = "product_crawler"

    spider: ClassVar[str]

    @classmethod
    def trigger(cls) -> List[str]:
        job_ids: List[str] = []
        for config in cls.make_spider_configs():
            job_id = trigger_spider(
                project_name=cls.project, spider_name=cls.spider, config=config
            )
            job_ids.append(job_id)
        return job_ids

    @classmethod
    @abstractmethod
    def make_spider_configs(cls) -> List[SpiderConfig]:
        raise NotImplementedError


class GscProductAnnouncementSpider(ProductAnnouncementSpider):
    spider: ClassVar[str] = "gsc_product"

    @classmethod
    def make_spider_configs(cls) -> List[SpiderConfig]:
        return [
            GscProductSpiderConfig(
                begin_year=JapanDatetimeHelper.today().year,
                end_year=JapanDatetimeHelper.today().year,
                category=GSCCategory.SCALE,
                is_announcement_spider=True,
            )
        ]


class AlterProductAnnouncementSpider(ProductAnnouncementSpider):
    spider: ClassVar[str] = "alter_product"

    @classmethod
    def make_spider_configs(cls) -> List[SpiderConfig]:
        return [
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


class NativeProductAnnouncementSpider(ProductAnnouncementSpider):
    spider: ClassVar[str] = "native_product"

    @classmethod
    def make_spider_configs(cls) -> List[SpiderConfig]:
        return [
            NativeProductSpiderConfig(
                end_page=1,
                category=NativeCategory.CHARACTERS,
                is_announcement_spider=True,
            ),
            NativeProductSpiderConfig(
                end_page=1,
                category=NativeCategory.CREATORS,
                is_announcement_spider=True,
            ),
        ]


class AmakuniProductAnnouncementSpider(ProductAnnouncementSpider):
    spider: ClassVar[str] = "amakuni_product"

    @classmethod
    def make_spider_configs(cls) -> List[SpiderConfig]:
        return [
            AmakuniProductSpiderConfig(
                is_announcement_spider=True, begin_year=JapanDatetimeHelper.today().year
            )
        ]
