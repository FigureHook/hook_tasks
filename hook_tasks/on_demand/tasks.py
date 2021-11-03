from figure_hook.Tasks.on_demand import send_discord_welcome_webhook as send_discord_webhook
from ..app import app


@app.task
def send_discord_welcome_webhook(webhook_id: int, webhook_token: str, msg: str):
    result = send_discord_webhook(webhook_id, webhook_token, msg)
    return result
