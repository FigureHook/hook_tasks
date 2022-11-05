import json
from typing import TYPE_CHECKING, Dict, Sequence

if TYPE_CHECKING:
    from discord.types.embed import Embed as EmbedDict

import redis
from discord import Embed

from hook_tasks.domains.sns_post.discord.errors import SetEmbedCacheFailed
from hook_tasks.domains.sns_post.discord.repositories.release_embed_cache_repository import (
    ReleaseEmbedCacheRepositoryInterface,
)
from hook_tasks.domains.sns_post.discord.value_objects.release_embed_cache import (
    ReleaseEmbedCache,
    ReleaseEmbedCacheKeyCriteria,
)


class ReleaseEmebedMeomoryCacheRepository(ReleaseEmbedCacheRepositoryInterface):
    cache: Dict[str, Sequence["EmbedDict"]]

    def __init__(self, *args, **kwargs) -> None:
        self.cache = {}
        super().__init__()

    def get_embed_cache(
        self, cache_key: ReleaseEmbedCacheKeyCriteria
    ) -> ReleaseEmbedCache | None:
        cache_value = self.cache.get(cache_key.to_key_str())
        if cache_value:
            return ReleaseEmbedCache(
                key=cache_key,
                value=[Embed.from_dict(embed_dict) for embed_dict in cache_value],
            )
        return None

    def set_embed_cache(
        self, cache_key: ReleaseEmbedCacheKeyCriteria, embeds: Sequence[Embed], ttl: int
    ) -> ReleaseEmbedCache:
        embed_dicts = [embed.to_dict() for embed in embeds]
        self.cache.setdefault(cache_key.to_key_str(), embed_dicts)
        return ReleaseEmbedCache(
            key=cache_key,
            value=embeds,
        )


class ReleaseEmbedRedisCacheRepository(ReleaseEmbedCacheRepositoryInterface):
    client: redis.Redis

    def __init__(self, client: redis.Redis) -> None:
        self.client = client

    def get_embed_cache(
        self, cache_key: ReleaseEmbedCacheKeyCriteria
    ) -> ReleaseEmbedCache | None:
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
    ) -> ReleaseEmbedCache:
        embed_dicts = [embed.to_dict() for embed in embeds]
        cache_value = json.dumps(embed_dicts)
        key = cache_key.to_key_str()
        if self.client.set(key, cache_value, exat=ttl):
            return ReleaseEmbedCache(key=cache_key, value=embeds)
        raise SetEmbedCacheFailed(key=cache_key)
