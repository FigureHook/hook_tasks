from abc import ABC, abstractmethod
from hashlib import md5
from typing import ClassVar

import requests as rq
from hook_tasks.api_clients import hook_api_client
from hook_tasks.helpers import JapanDatetimeHelper

from .entities.source_checksum import SourceChecksum
from .repositories.source_checksum_repository import SourceChecksumRepository


def _generate_checksum_value(target: bytes) -> str:
    m = md5()
    m.update(target)
    return m.hexdigest()


CHECKSUM_INIT_VALUE = "init"

checksum_repo = SourceChecksumRepository(api_client=hook_api_client)


class SiteSourceChceksum(ABC):
    __source_site__: ClassVar[str]

    _checksum: SourceChecksum
    _current_checksum_value: str
    _synchronizable: bool

    def __init__(self, checksum: SourceChecksum):
        if not self.__source_site__:
            raise ValueError("Class variable `__source_site__` should be set.")

        self._checksum = checksum
        self._current_checksum_value = CHECKSUM_INIT_VALUE
        self._synchronizable = False

    def _get_current_checksum_value(self) -> str:
        feature = self.extract_feature()
        self._current_checksum_value = _generate_checksum_value(feature)
        self._synchronizable = True
        return self._current_checksum_value

    def is_changed(self) -> bool:
        current_checksum = self._get_current_checksum_value()
        return self._checksum.value != current_checksum

    def sync(self):
        self._checksum.value = (
            self._current_checksum_value
            if self._synchronizable
            else self._get_current_checksum_value()
        )

        self._checksum = checksum_repo.save(self._checksum)

        return self

    @staticmethod
    @abstractmethod
    def extract_feature() -> bytes:
        raise NotImplementedError

    @classmethod
    def create(cls):
        checksum = checksum_repo.get_checksum_by_source(cls.__source_site__)
        if not checksum:
            checksum = checksum_repo.create_checksum(
                source_name=cls.__source_site__, checksum_value=CHECKSUM_INIT_VALUE
            )
        return cls(checksum=checksum)


class GscProductAnnouncementCheck(SiteSourceChceksum):
    __source_site__: ClassVar[str] = "gsc_product_announcement"

    @staticmethod
    def extract_feature() -> bytes:
        this_year = JapanDatetimeHelper.today().year
        url = f"https://www.goodsmile.info/ja/products/category/scale/announced/{this_year}"
        response = rq.get(url)
        response.raise_for_status()
        return response.content


class AlterProductAnnouncementCheck(SiteSourceChceksum):
    __source_site__: ClassVar[str] = "alter_product_announcement"

    @staticmethod
    def extract_feature() -> bytes:
        url = "https://www.alter-web.jp/products/"
        response = rq.get(url)
        response.raise_for_status()
        return response.content


class NativeProductAnnouncementCheck(SiteSourceChceksum):
    __source_site__: ClassVar[str] = "native_product_announcement"

    @staticmethod
    def extract_feature() -> bytes:
        url = f"https://www.native-web.jp/news/feed/"
        response = rq.head(url)
        etag = response.headers.get("ETag")
        response.raise_for_status()
        assert etag
        return etag.encode("utf-8")


class AmakuniProductAnnouncementCheck(SiteSourceChceksum):
    __source_site__: ClassVar[str] = "amakuni_product_announcement"

    @staticmethod
    def extract_feature() -> bytes:
        url = f"http://amakuni.info/index.php"
        response = rq.get(url)
        response.raise_for_status()
        return response.content
