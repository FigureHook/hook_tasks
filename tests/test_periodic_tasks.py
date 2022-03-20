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


@pytest.mark.usefixtures("db_session")
def test_check_new_release(mocker: MockerFixture):
    mocker.patch(
        "figure_hook.SourceChecksum.abcs.ProductAnnouncementChecksum._extract_feature"
    )
    mocker.patch(
        "figure_hook.SourceChecksum.abcs.ProductAnnouncementChecksum.is_changed",
        return_value=True
    )
    mocker.patch(
        "figure_hook.SourceChecksum.abcs.ProductAnnouncementChecksum.trigger_crawler",
        return_value=[1, 2, 3]
    )
    mocker.patch(
        "figure_hook.SourceChecksum.abcs.ProductAnnouncementChecksum.update"
    )

    from hook_tasks.periodic.tasks import check_new_release
    result = check_new_release.apply().get()
    assert result
