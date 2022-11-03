from typing import Any, List, Mapping

from celery import group
from celery.utils.functional import chunks
from celery.utils.log import get_task_logger

from hook_tasks.api_clients import hook_api_client
from hook_tasks.app import app
from hook_tasks.cache_clients import redis_client
from hook_tasks.domains.sns_post.discord.usecases import (
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
from hook_tasks.tasks.common.tasks import send_discord_embeds_webhook
from hook_tasks.tasks.sns_post.common.tasks import create_release_ticket_for_purpose

logger = get_task_logger(__name__)


@app.task
def push_new_release_to_discord_webhook():
    ticket_id = create_release_ticket_for_purpose.delay("discord_new_release").get()
    ticket_repo = ReleaseTicketRepository(api_client=hook_api_client)
    webhook_repo = DiscordWebhookRepository(client=hook_api_client)
    cache = ReleaseEmbedCacheRepository(client=redis_client)

    cache_usecase = PreheatEmbedCacheUseCase(
        ticket_repo=ticket_repo, webhook_repo=webhook_repo, cache=cache
    )
    cache_usecase.process_new_release_by_release_ticket_id(ticket_id=ticket_id)

    process_all_webhook_to_send_new_release_by_ticket_id.delay().get()


@app.task
def process_all_webhook_to_send_new_release_by_ticket_id(ticket_id: str):
    repo = DiscordWebhookRepository(client=hook_api_client)
    webhooks = repo.get_all_webhooks()
    group(
        process_new_release_discord_webhook_by_ticket_id.s(
            webhook_id=wb.id,
            webhook_token=wb.token,
            is_nsfw=wb.is_nsfw,
            lang=wb.lang,
            ticket_id=ticket_id,
        )
        for wb in webhooks
    )()


@app.task
def process_new_release_discord_webhook_by_ticket_id(
    webhook_id: str, webhook_token: str, is_nsfw: bool, lang: str, ticket_id: str
):
    cache = ReleaseEmbedCacheRepository(client=redis_client)
    cache_key = ReleaseEmbedCacheKeyCriteria(
        ticket_id=ticket_id, is_nsfw=is_nsfw, lang=lang
    )

    embed_cache = cache.get_embed_cache(cache_key=cache_key)
    if embed_cache:
        embeds_dicts: List[Mapping[str, Any]] = []
        for embed in embed_cache.value:
            embed = MakeEmbedTrackableUseCase.could_be_tracked_by_ticket_id(
                embed=embed, ticket_id=ticket_id
            )
            embeds_dicts.append(embed.to_dict())

        group(
            send_discord_embeds_webhook.s(
                webhook_id=webhook_id,
                webhook_token=webhook_token,
                embed_dicts=ten_embeds,
            )
            for ten_embeds in chunks(embeds_dicts, 10)
        )()
