from typing import Protocol, Sequence, Mapping, Any
from .model import ReleaseEmbedCacheKeyCriteria, ReleaseEmbedCache


class ReleaseEmbedCacheRepositoryInterface(Protocol):
    def get_embed_cache(
        self, cache_key: ReleaseEmbedCacheKeyCriteria
    ) -> ReleaseEmbedCache:
        raise NotImplementedError

    def set_embed_cache(
        self,
        cache_key: ReleaseEmbedCacheKeyCriteria,
        value: Sequence[Mapping[str, Any]],
        ttl: int,
    ) -> ReleaseEmbedCache:
        raise NotImplementedError
