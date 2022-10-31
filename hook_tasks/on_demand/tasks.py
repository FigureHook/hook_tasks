from typing import Any, Dict, Mapping, Sequence

from discord import Embed, HTTPException, SyncWebhook
from hook_tasks.api_clients import plurk_api
from hook_tasks.app import app
from hook_tasks.domains.sns_post.discord.create_embed_usecase import (
    create_welcome_embed,
)


@app.task(autoretry_for=(HTTPException,), max_retries=3)
def send_discord_welcome_webhook(webhook_id: int, webhook_token: str, msg: str):
    welcome_embed = create_welcome_embed(msg=msg)
    webhook = SyncWebhook.partial(id=webhook_id, token=webhook_token)
    webhook.send(embed=welcome_embed)


@app.task(autoretry_for=(HTTPException,), max_retries=5, retry_backoff=True)
def send_discord_embeds_webhook(
    webhook_id: int, webhook_token: str, embed_dicts: Sequence[Mapping[str, Any]]
):
    embeds = [Embed.from_dict(embed_dict) for embed_dict in embed_dicts]
    webhook = SyncWebhook.partial(id=webhook_id, token=webhook_token)
    webhook.send(embeds=embeds)


@app.task(bind=True)
def post_plurk(self, content: str, config: Dict[str, Any]):
    options = {content: content, **config}
    resp = plurk_api.callAPI("/APP/Timeline/plurkAdd", options=options)
    if not resp:
        """
        HTTP 400 BAD REQUEST with {"error_text": "Invalid data"} as body
        HTTP 400 BAD REQUEST with {"error_text": "Content is empty"} as body
        HTTP 400 BAD REQUEST with {"error_text": "no-permission-to-comment"} as body
        HTTP 400 BAD REQUEST with {"error_text": "anti-flood-same-content"} as body
        HTTP 400 BAD REQUEST with {"error_text": "anti-flood-spam-domain"} as body
        HTTP 400 BAD REQUEST with {"error_text": "anti-flood-too-many-new"} as body
        """
        self.retry(countdown=30, max_retries=3)

    return resp
