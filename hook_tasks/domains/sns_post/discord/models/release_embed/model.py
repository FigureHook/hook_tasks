from pydantic import BaseModel
from typing import Mapping, Sequence, Any


class ReleaseEmbedCacheKeyCriteria(BaseModel):
    ticket_id: str
    is_nsfw: bool
    lang: str

    def to_key_str(self):
        nsfw_str = "nsfw" if self.is_nsfw else "sfw"
        return f"{self.ticket_id}_{self.lang}_{nsfw_str}"


class ReleaseEmbedCache(BaseModel):
    key: ReleaseEmbedCacheKeyCriteria
    value: Sequence[Mapping[str, Any]]
