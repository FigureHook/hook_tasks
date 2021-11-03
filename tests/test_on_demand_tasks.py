import pytest
from faker import Faker
from pytest_mock import MockerFixture

fake = Faker()


def test_send_discord_welcome_webhook(mocker: MockerFixture):
    mock_send = mocker.patch(
        'figure_hook.Tasks.on_demand.send_discord_welcome_webhook'
    )
    from hook_tasks.on_demand.tasks import send_discord_welcome_webhook
    fake_wb_id = fake.random_int(min=10000, max=999999)
    fake_wb_token = fake.lexify(text="??????????")
    fake_msg = fake.sentence(nb_words=10)
    result = send_discord_welcome_webhook.apply(
        args=[
            fake_wb_id,
            fake_wb_token,
            fake_msg
        ]
    ).get()

    assert result
    mock_send.assert_called_once_with(fake_wb_id, fake_wb_token, fake_msg)
