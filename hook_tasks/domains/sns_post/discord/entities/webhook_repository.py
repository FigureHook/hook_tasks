from typing import Protocol, List

from .webhook import DiscordWebhook


class DiscordWebhookRepositoryInterface(Protocol):
    def get_all_langs(self) -> List[str]:
        raise NotImplementedError

    def get_all_webhooks(self) -> List[DiscordWebhook]:
        raise NotImplementedError

    def update_existed_status(self, webhook:DiscordWebhook, is_existed: bool) -> DiscordWebhook:
        raise NotImplementedError
