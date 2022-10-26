from abc import ABC, abstractmethod
from hashlib import md5
from typing import ClassVar

import requests as rq
from hook_tasks.helpers import JapanDatetimeHelper

from ..entities import DTOSourceChecksum
from ..repositories.checksum_repository import ChecksumRepository


def _generate_checksum_value(target: bytes) -> str:
    m = md5()
    m.update(target)
    return m.hexdigest()


class SiteSourceChceksum(ABC):
    __source_site__: ClassVar[str]

    _checksum_dto: DTOSourceChecksum
    _current_checksum_value: str
    _synchronizable: bool

    def __init__(self, checksum: DTOSourceChecksum):
        if not self.__source_site__:
            raise ValueError("Class variable `__source_site__` should be set.")

        self._checksum_dto = checksum
        self._current_checksum_value = "init"
        self._synchronizable = False

    def _get_current_checksum_value(self) -> str:
        feature = self.extract_feature()
        self._current_checksum_value = _generate_checksum_value(feature)
        self._synchronizable = True
        return self._current_checksum_value

    def is_changed(self) -> bool:
        current_checksum = self._get_current_checksum_value()
        return self._checksum_dto.value != current_checksum

    def sync(self):
        self._checksum_dto.value = (
            self._current_checksum_value
            if self._synchronizable
            else self._get_current_checksum_value()
        )

        if self._checksum_dto.id:
            self._checksum_dto = ChecksumRepository.update_checksum(
                source_checksum=self._checksum_dto
            )
        else:
            self._checksum_dto = ChecksumRepository.create_checksum(
                source_checksum=self._checksum_dto
            )

        return self

    @staticmethod
    @abstractmethod
    def extract_feature() -> bytes:
        raise NotImplementedError

    @classmethod
    def create(cls):
        checksum = ChecksumRepository.get_checksum_by_source(cls.__source_site__)
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
