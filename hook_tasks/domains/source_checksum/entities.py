from typing import Protocol, Optional
from typing_extensions import Self
from pydantic import BaseModel


class DTOSourceChecksum(BaseModel):
    id: Optional[int] = None
    source_name: str
    value: str = "init"


class SiteFeatureExtractable(Protocol):
    def is_changed(self) -> bool:
        raise NotImplementedError

    def sync(self) -> Self:
        raise NotImplementedError

    @staticmethod
    def extract_feature() -> bytes:
        raise NotImplementedError
