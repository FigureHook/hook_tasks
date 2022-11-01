from typing import Protocol, Sequence

from discord import Embed

from .model import ReleaseEmbedCache, ReleaseEmbedCacheKeyCriteria


class ReleaseEmbedCacheRepositoryInterface(Protocol):
    def get_embed_cache(
        self, cache_key: ReleaseEmbedCacheKeyCriteria
    ) -> ReleaseEmbedCache:
        raise NotImplementedError

    def set_embed_cache(
        self,
        cache_key: ReleaseEmbedCacheKeyCriteria,
        embeds: Sequence[Embed],
        ttl: int,
    ) -> ReleaseEmbedCache:
        raise NotImplementedError
