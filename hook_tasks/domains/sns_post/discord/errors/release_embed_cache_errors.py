from ..value_objects.release_embed_cache import ReleaseEmbedCacheKeyCriteria


class SetEmbedCacheFailed(Exception):
    def __init__(self, key: ReleaseEmbedCacheKeyCriteria) -> None:
        msg = f'Failed to set embed cache with key: "{key.to_key_str}".'
        super().__init__(msg)
