import json
from typing import Optional, Sequence

import redis
from discord import Embed
from hook_tasks.domains.sns_post.discord.models.release_embed.model import (
    ReleaseEmbedCache,
    ReleaseEmbedCacheKeyCriteria,
)
from hook_tasks.domains.sns_post.discord.models.release_embed.release_embed_cache_repository import (
    ReleaseEmbedCacheRepositoryInterface,
)


class ReleaseEmbedCacheRepository(ReleaseEmbedCacheRepositoryInterface):
    client: redis.Redis

    def __init__(self, client: redis.Redis) -> None:
        self.client = client

    def get_embed_cache(
        self, cache_key: ReleaseEmbedCacheKeyCriteria
    ) -> Optional[ReleaseEmbedCache]:
        value = self.client.get(cache_key.to_key_str())
        if value:
            cache_value = json.loads(value)
            return ReleaseEmbedCache(
                key=cache_key,
                value=[Embed.from_dict(embed_dict) for embed_dict in cache_value],
            )
        return None

    def set_embed_cache(
        self,
        cache_key: ReleaseEmbedCacheKeyCriteria,
        embeds: Sequence[Embed],
        ttl: int,
    ) -> Optional[ReleaseEmbedCache]:
        embed_dicts = [embed.to_dict() for embed in embeds]
        cache_value = json.dumps(embed_dicts)
        key = cache_key.to_key_str()
        if self.client.set(key, cache_value, exat=ttl):
            return ReleaseEmbedCache(key=cache_key, value=embeds)
