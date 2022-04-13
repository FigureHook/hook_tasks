import pytest
from pytest_mock import MockerFixture


@pytest.mark.usefixtures("db_session")
class TestNewsReleasesPush:
    def test_discord(self, mocker: MockerFixture):
        execution = mocker.patch(
            "figure_hook.Tasks.periodic.DiscordNewReleasePush.execute",
            return_value=True
        )

        from hook_tasks.periodic.tasks import push_discord_new_releases
        push_discord_new_releases.apply().get()
        execution.assert_called_once()

    def test_plurk(self, mocker: MockerFixture):
        execution = mocker.patch(
            "figure_hook.Tasks.periodic.PlurkNewReleasePush.execute",
            return_value=True
        )

        from hook_tasks.periodic.tasks import push_plurk_new_releases
        push_plurk_new_releases.apply().get()
        execution.assert_called_once()

@pytest.fixture
def mocked_checksum_method(mocker: MockerFixture):
    mocker.patch(
        "hook_tasks.SourceChecksum.abcs.BaseSourceSiteChecksum._extract_feature"
    )
    mocker.patch(
        "hook_tasks.SourceChecksum.abcs.BaseSourceSiteChecksum.is_changed",
        return_value=True
    )
    mocker.patch(
        "hook_tasks.SourceChecksum.abcs.BaseSourceSiteChecksum.update"
    )
    mocker.patch(
        "hook_tasks.SourceChecksum.abcs.BaseSourceSiteChecksumCanTriggerSpider.trigger_crawler",
        return_value=[1, 2, 3]
    )


@pytest.mark.usefixtures("db_session", "mocked_checksum_method")
def test_check_new_release(mocker: MockerFixture):
    from hook_tasks.periodic.tasks import check_new_release
    result = check_new_release.apply().get()
    assert result


@pytest.mark.usefixtures("db_session", "mocked_checksum_method")
def test_check_delay(mocker: MockerFixture):
    from hook_tasks.periodic.tasks import check_delay
    result = check_delay.apply().get()
    assert result
