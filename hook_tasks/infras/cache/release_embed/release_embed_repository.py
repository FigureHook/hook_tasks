import json
from typing import Any, Mapping, Optional, Sequence

import redis
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
            return ReleaseEmbedCache(key=cache_key, value=cache_value)
        return None

    def set_embed_cache(
        self,
        cache_key: ReleaseEmbedCacheKeyCriteria,
        value: Sequence[Mapping[str, Any]],
        ttl: int,
    ) -> Optional[ReleaseEmbedCache]:
        cache_value = json.dumps(value)
        key = cache_key.to_key_str()
        if self.client.set(key, cache_value, exat=ttl):
            return ReleaseEmbedCache(key=cache_key, value=value)
