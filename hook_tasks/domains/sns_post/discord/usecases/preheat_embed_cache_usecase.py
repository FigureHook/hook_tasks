from typing import List

from discord import Embed

from hook_tasks.domains.sns_post.common.repositories.release_ticket_repository import (
    ReleaseTicketRepositoryInterface,
)
from hook_tasks.domains.sns_post.discord.repositories.release_embed_cache_repository import (
    ReleaseEmbedCacheRepositoryInterface,
)
from hook_tasks.domains.sns_post.discord.repositories.webhook_repository import (
    DiscordWebhookRepositoryInterface,
)
from hook_tasks.domains.sns_post.discord.value_objects.release_embed_cache import (
    ReleaseEmbedCacheKeyCriteria,
)

from .create_embed_usecase import CreateEmbedUseCase
from .localize_embed_usecase import localize_release_embed_with_locale


class PreheatEmbedCacheUseCase:
    ticket_repo: ReleaseTicketRepositoryInterface[str]
    cache: ReleaseEmbedCacheRepositoryInterface
    webhook_repo: DiscordWebhookRepositoryInterface

    def __init__(
        self,
        ticket_repo: ReleaseTicketRepositoryInterface[str],
        webhook_repo: DiscordWebhookRepositoryInterface,
        cache: ReleaseEmbedCacheRepositoryInterface,
    ) -> None:
        self.ticket_repo = ticket_repo
        self.cache = cache
        self.webhook_repo = webhook_repo

    def process_new_release_by_release_ticket_id(
        self, ticket_id: str, ttl: int = 30 * 60
    ) -> str | None:
        release_feeds = self.ticket_repo.get_release_feeds_by_ticket_id(ticket_id)
        if not len(release_feeds):
            return None

        all_langs = self.webhook_repo.get_all_langs()
        for lang in all_langs:
            sfw_embeds: List[Embed] = []
            nsfw_embeds: List[Embed] = []
            for feed in release_feeds:
                release_embed = CreateEmbedUseCase.create_new_release_embed(
                    release_feed=feed
                )
                localized_embed = localize_release_embed_with_locale(
                    release_embed=release_embed, locale=lang
                )
                nsfw_embeds.append(localized_embed)
                if not feed.is_adult:
                    sfw_embeds.append(localized_embed)

            sfw_cache_key = ReleaseEmbedCacheKeyCriteria(
                ticket_id=ticket_id, is_nsfw=False, lang=lang
            )
            self.cache.set_embed_cache(
                cache_key=sfw_cache_key, embeds=sfw_embeds, ttl=ttl
            )

            nsfw_cache_key = ReleaseEmbedCacheKeyCriteria(
                ticket_id=ticket_id, is_nsfw=True, lang=lang
            )
            self.cache.set_embed_cache(
                cache_key=nsfw_cache_key, embeds=nsfw_embeds, ttl=ttl
            )

        return ticket_id
