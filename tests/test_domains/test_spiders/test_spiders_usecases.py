import pytest
from hook_tasks.domains.spiders.usecases.scrapy_spider import (
    GscProductAnnouncementSpiderUseCase,
    AlterProductAnnouncementSpiderUseCase,
    NativeProductAnnouncementSpiderUseCase,
    get_spiders_from_project,
    trigger_spider,
)
from pytest_mock import MockerFixture


def test_get_spiders(mocker: MockerFixture):
    mocker.patch(
        "hook_tasks.domains.spiders.usecases.scrapy_spider.get_spiders",
        new=mocker.MagicMock(return_value=["123"]),
    )
    for spider_name in get_spiders_from_project(project_name="project"):
        assert isinstance(spider_name, str)


def test_trigger_spider(mocker: MockerFixture):
    mocker.patch(
        "hook_tasks.domains.spiders.usecases.scrapy_spider.schedule",
        new=mocker.MagicMock(return_value="123a"),
    )
    assert isinstance(trigger_spider(project_name="project", spider_name="spider"), str)


def test_product_announcement_spider_usecase(mocker: MockerFixture):
    schedule_mock = mocker.MagicMock(return_value="123a")
    mocker.patch(
        "hook_tasks.domains.spiders.usecases.scrapy_spider.schedule",
        new=schedule_mock,
    )

    assert len(GscProductAnnouncementSpiderUseCase.trigger()) == 1
    assert len(AlterProductAnnouncementSpiderUseCase.trigger()) == 3
    assert len(NativeProductAnnouncementSpiderUseCase.trigger()) == 2
