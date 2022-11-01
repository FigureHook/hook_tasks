from hook_tasks.domains.sns_post.discord.entities.webhook_repository import (
    DiscordWebhookRepositoryInterface,
)
from hook_tasks.domains.sns_post.discord.entities.webhook import (
    DiscordWebhook,
    DiscordWebhookLocale,
)
from figure_hook_client.client import AuthenticatedClient
from typing import List
from figure_hook_client.api.discord import (
    get_webhooks_api_v1_webhooks_get,
    update_webhook_api_v1_webhooks_channel_id_put,
)
from figure_hook_client.models.webhook_create import WebhookCreate
from figure_hook_client.models.webhook_lang import WebhookLang
from figure_hook_client.types import UNSET, Unset


class DiscordWebhookRepository(DiscordWebhookRepositoryInterface):
    client: AuthenticatedClient

    def __init__(self, client: AuthenticatedClient) -> None:
        self.client = client

    def get_all_langs(self) -> List[DiscordWebhookLocale]:
        raise NotImplementedError

    def get_all_webhooks(self) -> List[DiscordWebhook]:
        webhooks = get_webhooks_api_v1_webhooks_get.sync(client=self.client)
        if webhooks:
            return [
                DiscordWebhook(
                    id=wb.id,
                    token=wb.decrypted_token,
                    lang=EmbedLocaleMapper.from_webhook_lang(wb.lang),
                    locale=EmbedLocaleMapper.from_webhook_lang(wb.lang),
                    channel_id=wb.channel_id,
                    is_nsfw=bool(wb.is_nsfw),
                    is_existed=bool(wb.is_existed),
                )
                for wb in webhooks
            ]
        return []

    def update_existed_status(
        self, webhook: DiscordWebhook, is_existed: bool
    ) -> DiscordWebhook:
        raise NotImplementedError


_lang_mapping = {
    WebhookLang.EN: DiscordWebhookLocale.EN,
    WebhookLang.JA: DiscordWebhookLocale.JA,
    WebhookLang.ZH_TW: DiscordWebhookLocale.ZH_TW,
}


class EmbedLocaleMapper:
    @staticmethod
    def from_webhook_lang(webhook_lang: WebhookLang | Unset) -> DiscordWebhookLocale:
        if isinstance(webhook_lang, Unset):
            return DiscordWebhookLocale.EN
        return _lang_mapping.get(webhook_lang, DiscordWebhookLocale.EN)
