from typing import Protocol, List

from ..entities.webhook import DiscordWebhook, DiscordWebhookLocale


class DiscordWebhookRepositoryInterface(Protocol):
    def get_all_langs(self) -> List[DiscordWebhookLocale]:
        raise NotImplementedError

    def get_all_webhooks(self) -> List[DiscordWebhook]:
        raise NotImplementedError

    def update_existed_status_by_webhook_id(
        self, webhook_id: str, is_existed: bool
    ) -> DiscordWebhook:
        raise NotImplementedError
