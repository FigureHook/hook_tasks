from typing import Any, List, Mapping

from celery import group
from celery.utils.functional import chunks
from celery.utils.log import get_task_logger

from hook_tasks.api_clients import hook_api_client
from hook_tasks.app import app
from hook_tasks.cache_clients import redis_client
from hook_tasks.domains.sns_post.discord.use_cases import (
    MakeEmbedTrackableUseCase,
    PreheatEmbedCacheUseCase,
)
from hook_tasks.domains.sns_post.discord.value_objects.release_embed_cache import (
    ReleaseEmbedCacheKeyCriteria,
)
from hook_tasks.infras.cache.release_embed.release_embed_repository import (
    ReleaseEmbedCacheRepository,
)
from hook_tasks.infras.persistance.discord_webhook.discord_webhook_repository import (
    DiscordWebhookRepository,
)
from hook_tasks.infras.persistance.release_ticket.release_ticket_repository import (
    ReleaseTicketRepository,
)
from ..common.tasks import send_discord_embeds_webhook
from hook_tasks.domains.sns_post.common.use_cases.create_release_ticket_use_case import (
    CreateReleaseTicketUseCase,
)

logger = get_task_logger(__name__)


@app.task
def push_new_release_to_discord_webhook():
    ticket_repo = ReleaseTicketRepository(api_client=hook_api_client)
    ticket_use_case = CreateReleaseTicketUseCase(ticket_repo=ticket_repo)

    ticket_id = ticket_use_case.create_release_ticket_for_purpose("discord_new_release")

    webhook_repo = DiscordWebhookRepository(client=hook_api_client)
    cache = ReleaseEmbedCacheRepository(client=redis_client)
    cache_usecase = PreheatEmbedCacheUseCase(
        ticket_repo=ticket_repo, webhook_repo=webhook_repo, cache=cache
    )

    cache_usecase.process_new_release_by_release_ticket_id(ticket_id=ticket_id)
    webhooks = webhook_repo.get_all_webhooks()

    webhook_tasks = []
    for webhook in webhooks:
        cache_key = ReleaseEmbedCacheKeyCriteria(
            ticket_id=ticket_id, is_nsfw=webhook.is_nsfw, lang=webhook.lang
        )
        embed_cache = cache.get_embed_cache(cache_key=cache_key)
        if embed_cache:
            embeds_dicts: List[Mapping[str, Any]] = []
            for embed in embed_cache.value:
                embed = MakeEmbedTrackableUseCase.could_be_tracked_by_ticket_id(
                    embed=embed, ticket_id=ticket_id
                )
                embeds_dicts.append(embed.to_dict())

            for ten_embeds in chunks(embeds_dicts, 10):
                webhook_tasks.append(
                    send_discord_embeds_webhook.s(
                        webhook_id=webhook.id,
                        webhook_token=webhook.token,
                        embed_dicts=ten_embeds,
                    )
                )

    group(webhook_tasks).apply_async()
