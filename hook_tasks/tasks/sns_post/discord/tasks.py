import random
import time
from typing import List

from celery import group, chain
from celery.utils.functional import chunks
from celery.utils.log import get_task_logger
from discord import Embed
from hook_tasks.api_clients import hook_api_client
from hook_tasks.app import app
from hook_tasks.cache_clients import redis_client
from hook_tasks.domains.sns_post.discord.create_embed_usecase import (
    create_new_release_embed,
)
from hook_tasks.domains.sns_post.discord.localize_embed_usecase import (
    localize_release_embed_with_locale,
)
from hook_tasks.domains.sns_post.discord.set_embed_tracking_footer import (
    set_release_embed_tracking_footer,
)
from hook_tasks.domains.sns_post.discord.value_objects.release_embed_cache import (
    ReleaseEmbedCacheKeyCriteria,
)
from hook_tasks.domains.sns_post.plurk.create_plurk_usecase import (
    create_new_release_plurk_by_release_feed,
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
    ticket = create_release_ticket_for_purpose.s("discord_new_release").apply_async()
    ticket_id = ticket.get()

    if ticket_id:
        chain(
            create_embed_data_cache.s(ticket_id),
            process_all_webhook_to_send_new_release_by_ticket_id.s(),
        )()


@app.task
def process_all_webhook_to_send_new_release_by_ticket_id(ticket_id: str | None):
    if ticket_id:
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
        embeds_dicts = []
        for embed in embed_cache.value:
            embed = set_release_embed_tracking_footer(embed=embed, ticket_id=ticket_id)
            embeds_dicts.append(embed.to_dict())

        group(
            send_discord_embeds_webhook.s(
                webhook_id=webhook_id,
                webhook_token=webhook_token,
                embed_dicts=ten_embeds,
            )
            for ten_embeds in chunks(embeds_dicts, 10)
        )()


@app.task
def create_embed_data_cache(ticket_id: str) -> str | None:
    cache_ttl = 30 * 60
    ticket_repo = ReleaseTicketRepository(api_client=hook_api_client)
    webhook_repo = DiscordWebhookRepository(client=hook_api_client)
    cache = ReleaseEmbedCacheRepository(client=redis_client)

    release_feeds = ticket_repo.get_release_feeds_by_ticket_id(ticket_id)
    all_langs = webhook_repo.get_all_langs()

    if not len(release_feeds):
        return None

    for lang in all_langs:
        sfw_embeds: List[Embed] = []
        nsfw_embeds: List[Embed] = []
        for feed in release_feeds:
            release_embed = create_new_release_embed(release_feed=feed)
            localized_embed = localize_release_embed_with_locale(
                release_embed=release_embed, locale=lang
            )
            nsfw_embeds.append(localized_embed)
            if not feed.is_adult:
                sfw_embeds.append(localized_embed)

        sfw_cache_key = ReleaseEmbedCacheKeyCriteria(
            ticket_id=ticket_id, is_nsfw=False, lang=lang
        )
        cache.set_embed_cache(cache_key=sfw_cache_key, embeds=sfw_embeds, ttl=cache_ttl)

        nsfw_cache_key = ReleaseEmbedCacheKeyCriteria(
            ticket_id=ticket_id, is_nsfw=True, lang=lang
        )
        cache.set_embed_cache(
            cache_key=nsfw_cache_key, embeds=nsfw_embeds, ttl=cache_ttl
        )

    return ticket_id
