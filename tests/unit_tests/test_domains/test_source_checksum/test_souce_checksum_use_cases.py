from pydantic_factories import ModelFactory
from pydantic_factories.plugins.pytest_plugin import register_fixture
from pytest_mock import MockerFixture

from hook_tasks.domains.source_checksum.announcement_check_use_case import (
    AlterProductAnnouncementCheck,
    AmakuniProductAnnouncementCheck,
    GscProductAnnouncementCheck,
    NativeProductAnnouncementCheck,
)
from hook_tasks.domains.source_checksum.entities.source_checksum import SourceChecksum
from hook_tasks.domains.source_checksum.repositories.source_checksum_repository import (
    SourceChecksumRepositoryInterface,
)

all_checks = (
    GscProductAnnouncementCheck,
    AlterProductAnnouncementCheck,
    NativeProductAnnouncementCheck,
    AmakuniProductAnnouncementCheck,
)


@register_fixture
class SourceChecksumFactory(ModelFactory):
    """SourceChecksum factory"""

    __model__ = SourceChecksum


def test_check_checksum(mocker: MockerFixture, source_checksum_factory):
    for check in all_checks:
        mock_checksum: SourceChecksum = source_checksum_factory.build()
        mock_checksum.source_name = check.__source_site__

        class MockChecksumRepo(SourceChecksumRepositoryInterface):
            def save(self, source_checksum: SourceChecksum) -> SourceChecksum:
                return source_checksum

            def create_checksum(
                self, source_name: str, checksum_value: str
            ) -> SourceChecksum:
                return SourceChecksum(
                    id=1, source_name=source_name, value=checksum_value
                )

            def get_checksum_by_source(self, source_name: str) -> SourceChecksum | None:
                return mock_checksum

        announcement_check = check(checksum_repo=MockChecksumRepo())  # type: ignore
        mocker.patch(
            "hook_tasks.domains.source_checksum.announcement_check_use_case._generate_checksum_value",
            new=mocker.MagicMock(return_value=mock_checksum.value),
        )
        assert not announcement_check.is_changed()

        mocker.patch(
            "hook_tasks.domains.source_checksum.announcement_check_use_case._generate_checksum_value",
            new=mocker.MagicMock(return_value="321"),
        )
        assert announcement_check.is_changed()


def test_sync_checksum(mocker: MockerFixture, source_checksum_factory):
    for check in all_checks:
        mock_checksum: SourceChecksum = source_checksum_factory.build()
        mock_checksum.source_name = check.__source_site__

        class MockChecksumRepo(SourceChecksumRepositoryInterface):
            def save(self, source_checksum: SourceChecksum) -> SourceChecksum:
                return source_checksum

            def create_checksum(
                self, source_name: str, checksum_value: str
            ) -> SourceChecksum:
                return SourceChecksum(
                    id=1, source_name=source_name, value=checksum_value
                )

            def get_checksum_by_source(self, source_name: str) -> SourceChecksum | None:
                return mock_checksum

        mocker.patch.object(
            check,
            attribute="_get_current_checksum_value",
            new=mocker.MagicMock(return_value="321"),
        )
        another_mock_dto = mock_checksum.copy()
        another_mock_dto.value = "321"
        mocker.patch.object(
            target=MockChecksumRepo,
            attribute="save",
            new=mocker.MagicMock(return_value=another_mock_dto),
        )
        mocker.patch.object(
            target=MockChecksumRepo,
            attribute="create_checksum",
            new=mocker.MagicMock(return_value=another_mock_dto),
        )
        announcement_check = check(checksum_repo=MockChecksumRepo())  # type: ignore
        assert not announcement_check.sync().is_changed()
