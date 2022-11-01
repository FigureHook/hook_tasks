from typing import List

from figure_hook_client.api.discord import (
    get_webhooks_api_v1_webhooks_get,
    patch_webhook_api_v1_webhooks_webhook_id_patch,
)
from figure_hook_client.client import AuthenticatedClient
from figure_hook_client.models.decrypted_webhook_in_db import DecryptedWebhookInDB
from figure_hook_client.models.webhook_lang import WebhookLang
from figure_hook_client.models.webhook_update import WebhookUpdate
from figure_hook_client.types import Unset
from hook_tasks.domains.sns_post.discord.entities.webhook import (
    DiscordWebhook,
    DiscordWebhookLocale,
)
from hook_tasks.domains.sns_post.discord.entities.webhook_repository import (
    DiscordWebhookRepositoryInterface,
)


class DiscordWebhookRepository(DiscordWebhookRepositoryInterface):
    client: AuthenticatedClient

    def __init__(self, client: AuthenticatedClient) -> None:
        self.client = client

    def get_all_langs(self) -> List[DiscordWebhookLocale]:
        webhooks = get_webhooks_api_v1_webhooks_get.sync(client=self.client)
        if webhooks:
            return list(
                set(
                    DiscordWebhookLocaleMapper.from_webhook_lang(wb.lang)
                    for wb in webhooks
                )
            )
        raise NotImplementedError

    def get_all_webhooks(self) -> List[DiscordWebhook]:
        webhooks = get_webhooks_api_v1_webhooks_get.sync(client=self.client)
        if webhooks:
            return [
                DiscordWebhookMapper.from_decrypted_webhook_in_db(wb) for wb in webhooks
            ]
        return []

    def update_existed_status_by_webhook_id(
        self, webhook_id: str, is_existed: bool
    ) -> DiscordWebhook:
        webhook_patch = WebhookUpdate(is_existed=is_existed)
        patched_webhook = patch_webhook_api_v1_webhooks_webhook_id_patch.sync(
            webhook_id=webhook_id, client=self.client, json_body=webhook_patch
        )
        if isinstance(patched_webhook, DecryptedWebhookInDB):
            return DiscordWebhookMapper.from_decrypted_webhook_in_db(patched_webhook)

        raise NotImplementedError


class DiscordWebhookMapper:
    @staticmethod
    def from_decrypted_webhook_in_db(
        db_webhook: DecryptedWebhookInDB,
    ) -> DiscordWebhook:
        return DiscordWebhook(
            id=db_webhook.id,
            token=db_webhook.decrypted_token,
            lang=DiscordWebhookLocaleMapper.from_webhook_lang(db_webhook.lang),
            locale=DiscordWebhookLocaleMapper.from_webhook_lang(db_webhook.lang),
            channel_id=db_webhook.channel_id,
            is_nsfw=bool(db_webhook.is_nsfw),
            is_existed=bool(db_webhook.is_existed),
        )


_lang_mapping = {
    WebhookLang.EN: DiscordWebhookLocale.EN,
    WebhookLang.JA: DiscordWebhookLocale.JA,
    WebhookLang.ZH_TW: DiscordWebhookLocale.ZH_TW,
}


class DiscordWebhookLocaleMapper:
    @staticmethod
    def from_webhook_lang(webhook_lang: WebhookLang | Unset) -> DiscordWebhookLocale:
        if isinstance(webhook_lang, Unset):
            return DiscordWebhookLocale.EN
        return _lang_mapping.get(webhook_lang, DiscordWebhookLocale.EN)
