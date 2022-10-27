from abc import ABC
from dataclasses import asdict, dataclass
from typing import Optional, Union

from figure_parser.enums import AlterCategory, GSCCategory, GSCLang, NativeCategory


@dataclass
class SpiderConfig(ABC):
    def asdict(self):
        return asdict(self)


@dataclass
class EmptyConfig(SpiderConfig):
    ...


@dataclass
class ProductSpiderConfig(SpiderConfig):
    force_update: bool = False
    is_announcement_spider: bool = False


@dataclass
class GscProductSpiderConfig(ProductSpiderConfig):
    begin_year: Optional[int] = None
    end_year: Optional[int] = None
    lang: Optional[Union[GSCLang, str]] = GSCLang.JAPANESE
    category: Optional[Union[GSCCategory, str]] = GSCCategory.SCALE


@dataclass
class AlterProductSpiderConfig(ProductSpiderConfig):
    begin_year: Optional[int] = None
    end_year: Optional[int] = None
    category: Optional[Union[AlterCategory, str]] = AlterCategory.ALTAIR


@dataclass
class NativeProductSpiderConfig(ProductSpiderConfig):
    begin_page: int = 1
    end_page: Optional[int] = None
    category: Optional[Union[NativeCategory, str]] = NativeCategory.CHARACTERS


@dataclass
class AmakuniProductSpiderConfig(ProductSpiderConfig):
    begin_year: int = 2012
    end_year: Optional[int] = None
