from typing import Type

import pytest
from figure_hook.utils.scrapyd_api import ScrapydUtil
from hook_tasks.SourceChecksum.abcs import \
    BaseSourceSiteChecksumCanTriggerSpider
from pytest_mock import MockerFixture


@pytest.mark.usefixtures("db_session")
class BaseTestAnnouncementChecksum:
    __checksum_cls__: Type[BaseSourceSiteChecksumCanTriggerSpider]

    @pytest.fixture
    def site_checksum(self, db_session):
        util = ScrapydUtil("http://localhost:8000", "project")
        site_checksum = self.__checksum_cls__(util)
        return site_checksum

    @pytest.mark.usefixtures("site_checksum")
    def test_property(self, site_checksum: BaseSourceSiteChecksumCanTriggerSpider):
        assert hasattr(site_checksum, "current")
        assert hasattr(site_checksum, "previous")
        assert hasattr(site_checksum, "is_changed")
        assert hasattr(site_checksum, "feature")
        assert hasattr(site_checksum, 'spider_configs')
        if isinstance(site_checksum.feature, list):
            assert all(isinstance(feature, bytes)
                       for feature in site_checksum.feature)
        else:
            assert isinstance(site_checksum.feature, bytes)

    @pytest.mark.usefixtures("site_checksum")
    def test_checksum_should_be_different_at_firsttime(self, site_checksum: BaseSourceSiteChecksumCanTriggerSpider):
        assert site_checksum.is_changed, "`previous` and `current` shoud be different at firsttime."

    @pytest.mark.usefixtures("site_checksum")
    def test_checksum_should_not_be_changed_after_updated(self, site_checksum: BaseSourceSiteChecksumCanTriggerSpider):
        site_checksum.update()
        assert not site_checksum.is_changed, "`previous` and `current` should be same after checksum updated."

    @pytest.mark.usefixtures("site_checksum")
    def test_trigger_crawler(self, mocker: MockerFixture, site_checksum: BaseSourceSiteChecksumCanTriggerSpider):
        crawler_trigger = mocker.patch(
            "figure_hook.utils.scrapyd_api.ScrapydUtil.schedule_spider",
            return_value="job"
        )

        jobs = site_checksum.trigger_crawler()
        spider_configs = [
            config.asdict()
            for config in site_checksum.spider_configs
        ]
        assert isinstance(jobs, list)
        assert crawler_trigger.call_count == len(jobs)
        for call_args in crawler_trigger.call_args_list:
            assert site_checksum.__spider__ in call_args.args
            assert call_args.kwargs["settings"] in spider_configs
