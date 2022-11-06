from pytest_mock import MockerFixture

from hook_tasks.domains.spiders.scrapy_spider_use_case import (
    AlterProductAnnouncementSpider,
    AmakuniProductAnnouncementSpider,
    GscProductAnnouncementSpider,
    NativeProductAnnouncementSpider,
    get_spiders_from_project,
    trigger_spider,
)


def test_get_spiders(mocker: MockerFixture):
    mocker.patch(
        "hook_tasks.domains.spiders.scrapy_spider_use_case.get_spiders",
        new=mocker.MagicMock(return_value=["123"]),
    )
    for spider_name in get_spiders_from_project(project_name="project"):
        assert isinstance(spider_name, str)


def test_trigger_spider(mocker: MockerFixture):
    mocker.patch(
        "hook_tasks.domains.spiders.scrapy_spider_use_case.schedule",
        new=mocker.MagicMock(return_value="123a"),
    )
    assert isinstance(trigger_spider(project_name="project", spider_name="spider"), str)


def test_product_announcement_spider_usecase(mocker: MockerFixture):
    schedule_mock = mocker.MagicMock(return_value="123a")
    mocker.patch(
        "hook_tasks.domains.spiders.scrapy_spider_use_case.schedule",
        new=schedule_mock,
    )

    assert len(GscProductAnnouncementSpider.trigger()) == 1
    assert len(AlterProductAnnouncementSpider.trigger()) == 3
    assert len(NativeProductAnnouncementSpider.trigger()) == 2
    assert len(AmakuniProductAnnouncementSpider.trigger()) == 1