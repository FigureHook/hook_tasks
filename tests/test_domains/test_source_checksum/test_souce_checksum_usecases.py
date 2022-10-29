from hook_tasks.domains.source_checksum.entities import SourceChecksum
from hook_tasks.domains.source_checksum.announcement_check_usecase import (
    AlterProductAnnouncementCheck,
    AmakuniProductAnnouncementCheck,
    GscProductAnnouncementCheck,
    NativeProductAnnouncementCheck,
)
from pydantic_factories import ModelFactory
from pydantic_factories.plugins.pytest_plugin import register_fixture
from pytest_mock import MockerFixture

all_checks = (
    GscProductAnnouncementCheck,
    AlterProductAnnouncementCheck,
    NativeProductAnnouncementCheck,
    AmakuniProductAnnouncementCheck,
)


@register_fixture
class DtoSourceChecksumFactory(ModelFactory):
    """DTOSourceChecksum factory"""

    __model__ = SourceChecksum


def test_check_checksum(mocker: MockerFixture, dto_source_checksum_factory):
    for check in all_checks:
        mock_dto: SourceChecksum = dto_source_checksum_factory.build()
        mock_dto.source_name = check.__source_site__
        mocker.patch(
            "hook_tasks.domains.source_checksum.announcement_check_usecase.SourceChecksumRepository.get_checksum_by_source",
            new=mocker.MagicMock(return_value=mock_dto),
        )
        announcement_check = check.create()
        mocker.patch(
            "hook_tasks.domains.source_checksum.announcement_check_usecase._generate_checksum_value",
            new=mocker.MagicMock(return_value=mock_dto.value),
        )
        assert not announcement_check.is_changed()

        mocker.patch(
            "hook_tasks.domains.source_checksum.announcement_check_usecase._generate_checksum_value",
            new=mocker.MagicMock(return_value="321"),
        )


def test_sync_checksum(mocker: MockerFixture, dto_source_checksum_factory):
    for check in all_checks:
        mock_dto: SourceChecksum = dto_source_checksum_factory.build()
        mock_dto.source_name = check.__source_site__
        mocker.patch(
            "hook_tasks.domains.source_checksum.announcement_check_usecase.SourceChecksumRepository.get_checksum_by_source",
            new=mocker.MagicMock(return_value=mock_dto),
        )
        mocker.patch.object(
            check,
            attribute="_get_current_checksum_value",
            new=mocker.MagicMock(return_value="321"),
        )
        another_mock_dto = mock_dto.copy()
        another_mock_dto.value = "321"
        mocker.patch(
            "hook_tasks.domains.source_checksum.announcement_check_usecase.SourceChecksumRepository.save",
            new=mocker.MagicMock(return_value=another_mock_dto),
        )
        mocker.patch(
            "hook_tasks.domains.source_checksum.announcement_check_usecase.SourceChecksumRepository.create_checksum",
            new=mocker.MagicMock(return_value=another_mock_dto),
        )
        announcement_check = check.create()
        assert not announcement_check.sync().is_changed()
