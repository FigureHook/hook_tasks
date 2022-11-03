from typing import Protocol

from ..entities.source_checksum import SourceChecksum


class SourceChecksumRepositoryInterface(Protocol):
    def create_checksum(self, source_name: str, checksum_value: str) -> SourceChecksum:
        raise NotImplementedError

    def get_checksum_by_source(self, source_name: str) -> SourceChecksum | None:
        raise NotImplementedError

    def save(self, source_checksum: SourceChecksum) -> SourceChecksum:
        raise NotImplementedError
