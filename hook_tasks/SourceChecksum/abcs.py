import functools
from abc import ABC, abstractmethod
from hashlib import md5
from typing import List, TypeVar, Union

from figure_hook.Models.source_checksum import SourceChecksum
from figure_hook.utils.scrapyd_api import ScrapydUtil

from .spider_config import SpiderConfig

__all__ = ["BaseSourceSiteChecksum",
           "ProductAnnouncementChecksum", "ShipmentChecksum"]


ChecksumFeature = Union[bytes, List[bytes]]


class BaseSourceSiteChecksum(ABC):
    """SourceSiteChecksum abstract class"""

    # source site identifier in database
    __source_site__: str
    # checksum orm model
    __source_checksum: SourceChecksum
    # extracted feature to check the site was changed or not
    _feature: ChecksumFeature

    def __init__(self) -> None:
        check_class_attribute(self, "__source_site__")
        check_class_attribute(self, "__source_checksum")

        site_checksum = SourceChecksum.get_by_site(
            self.__source_site__) or SourceChecksum(source=self.__source_site__, checksum='init').save()

        self.__source_checksum = site_checksum
        self.extract_feature()

    @property
    def feature(self) -> ChecksumFeature:
        return self._feature

    @property
    def current(self) -> str:
        if isinstance(self.feature, list):
            return generate_checksum(*self.feature)
        return generate_checksum(self.feature)

    @property
    def previous(self) -> str:
        return self.__source_checksum.checksum

    @property
    def is_changed(self) -> bool:
        return self.current != self.previous

    def update(self):
        self.__source_checksum.update(checksum=self.current)  # type: ignore

    def extract_feature(self):
        self._feature = self._extract_feature()

    @abstractmethod
    def _extract_feature(self) -> ChecksumFeature:
        """Return any bytes which could identify the site has changed."""


class BaseSourceSiteChecksumCanTriggerSpider(BaseSourceSiteChecksum, ABC):
    # Name of the target spider.
    __spider__: str
    # instance of :class:`figure_hook.utils.scrapyd_api.ScrapydUtil`
    scrapyd_util: ScrapydUtil

    def __init__(self, scrapyd_util: ScrapydUtil) -> None:
        check_class_attribute(self, "__spider__")
        self.scrapyd_util = scrapyd_util
        super().__init__()

    @property
    @abstractmethod
    def spider_configs(self) -> List[SpiderConfig]: ...

    def trigger_crawler(self) -> List:
        """Trigger the spiders to parse new product."""
        jobs = []
        for config in self.spider_configs:
            spider_name = self.__spider__
            job = self.scrapyd_util.schedule_spider(
                spider_name, settings=config.asdict())
            jobs.append(job)

        return jobs


class ProductAnnouncementChecksum(BaseSourceSiteChecksumCanTriggerSpider, ABC):
    ...


class ShipmentChecksum(BaseSourceSiteChecksumCanTriggerSpider, ABC):
    ...


class DelayChecksum(BaseSourceSiteChecksumCanTriggerSpider, ABC):
    ...


@functools.lru_cache
def generate_checksum(*target) -> str:
    m = md5()
    for t in target:
        m.update(t)
    return m.hexdigest()


T = TypeVar('T')


def check_class_attribute(instance: T, attr_name: str) -> T:
    """
    :raises NotImplementedError:
    """
    if not hasattr(instance, "__source_site__"):
        raise NotImplementedError(
            f"Class attribute `{attr_name}` should be implemented."
        )

    return instance
