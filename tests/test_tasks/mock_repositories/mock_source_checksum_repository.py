from hook_tasks.domains.source_checksum.repositories.source_checksum_repository import (
    SourceChecksumRepositoryInterface,
    SourceChecksum,
)


class MockSourceChecksumRepository(SourceChecksumRepositoryInterface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def get_checksum_by_source(self, source_name: str) -> SourceChecksum | None:
        return None

    def save(self, source_checksum: SourceChecksum) -> SourceChecksum:
        return source_checksum

    def create_checksum(self, source_name: str, checksum_value: str) -> SourceChecksum:
        return SourceChecksum(id=1, source_name=source_name, value=checksum_value)
