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
