from itertools import chain

from pytest_mock import MockerFixture

from hook_tasks.tasks.new_release_check.tasks import (
    check_new_release,
    check_new_release_by_site_name,
)

from .mock_repositories.mock_source_checksum_repository import (
    MockSourceChecksumRepository,
)


def test_check_new_release(celery_app, celery_worker, mocker: MockerFixture):
    mocker.patch(
        "hook_tasks.tasks.new_release_check.tasks.SourceChecksumRepository",
        new=MockSourceChecksumRepository,
    )
    mocker.patch(
        "hook_tasks.tasks.new_release_check.tasks.ProductAnnouncementSpider.trigger",
        return_value=["123"],
    )

    r = check_new_release()
    result = r.get()
    assert "123" in chain.from_iterable(result)


def test_check_new_release_by_site_name(mocker: MockerFixture):
    mocker.patch(
        "hook_tasks.tasks.new_release_check.tasks.SourceChecksumRepository",
        new=MockSourceChecksumRepository,
    )
    mocker.patch(
        "hook_tasks.tasks.new_release_check.tasks.ProductAnnouncementSpider.trigger",
        return_value=["123"],
    )
    task_result = check_new_release_by_site_name("amakuni")
    assert isinstance(task_result, list)
