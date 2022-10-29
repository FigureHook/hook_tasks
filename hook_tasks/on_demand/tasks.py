from typing import Any, Dict

from discord import SyncWebhook
from hook_tasks.api_clients import plurk_api
from hook_tasks.app import app
from hook_tasks.domains.sns_post.discord.create_embed_usecase import (
    create_welcome_embed,
)


@app.task
def send_discord_welcome_webhook(webhook_id: int, webhook_token: str, msg: str):
    welcome_embed = create_welcome_embed(msg=msg)
    webhook = SyncWebhook.partial(id=webhook_id, token=webhook_token)
    webhook.send(embed=welcome_embed)


@app.task(bind=True)
def post_plurk(self, content: str, config: Dict[str, Any]):
    options = {content: content, **config}
    resp = plurk_api.callAPI("/APP/Timeline/plurkAdd", options=options)
    if not resp:
        self.retry(countdown=30, max_retries=3)
    return resp
