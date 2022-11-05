from typing import Iterator

from celery import group
from celery.utils.functional import chunks
from celery.utils.log import get_task_logger

from hook_tasks.api_clients import hook_api_client
from hook_tasks.app import app
from hook_tasks.domains.sns_post.common.use_cases.create_release_ticket_use_case import (
    CreateReleaseTicketUseCase,
)
from hook_tasks.domains.sns_post.discord.use_cases import PreheatEmbedCacheUseCase
from hook_tasks.domains.sns_post.discord.value_objects.release_embed_cache import (
    ReleaseEmbedCacheKeyCriteria,
)
from hook_tasks.infras.cache.release_embed.release_embed_repository import (
    ReleaseEmebedMeomoryCacheRepository,
)
from hook_tasks.infras.persistance.discord_webhook.discord_webhook_repository import (
    DiscordWebhookRepository,
)
from hook_tasks.infras.persistance.release_ticket.release_ticket_repository import (
    ReleaseTicketRepository,
)

from ..common.tasks import send_discord_embeds_webhook

logger = get_task_logger(__name__)


@app.task
def push_new_release_to_discord_webhook():
    cache = ReleaseEmebedMeomoryCacheRepository()
    ticket_repo = ReleaseTicketRepository(api_client=hook_api_client)
    webhook_repo = DiscordWebhookRepository(client=hook_api_client)

    ticket_use_case = CreateReleaseTicketUseCase(ticket_repo=ticket_repo)
    cache_usecase = PreheatEmbedCacheUseCase(
        ticket_repo=ticket_repo, webhook_repo=webhook_repo, cache=cache
    )

    ticket_id = ticket_use_case.create_release_ticket_for_purpose("discord_new_release")
    ticket_id = cache_usecase.process_new_release_by_release_ticket_id(
        ticket_id=ticket_id
    )

    if not ticket_id:
        return None

    # TODO: When the webhooks grow up, this work should be seperated.
    webhooks = webhook_repo.get_all_webhooks()
    webhook_tasks = []
    for webhook in webhooks:
        cache_key = ReleaseEmbedCacheKeyCriteria(
            ticket_id=ticket_id, is_nsfw=webhook.is_nsfw, lang=webhook.lang
        )
        embed_cache = cache.get_embed_cache(cache_key=cache_key)
        if not embed_cache:
            continue

        embeds_dicts: Iterator = map(lambda e: e.to_dict(), embed_cache.value)
        # *INFO: Temporarily set lengh of chunk to 1, need to be increased when hit the rate limit.
        for embeds_batch in chunks(embeds_dicts, 1):
            webhook_tasks.append(
                send_discord_embeds_webhook.s(
                    webhook_id=webhook.id,
                    webhook_token=webhook.token,
                    embed_dicts=embeds_batch,
                )
            )

    if len(webhook_tasks):
        group(webhook_tasks).apply_async()
