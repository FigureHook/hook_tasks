from dataclasses import dataclass
from typing import Sequence

from discord import Embed
from pydantic import BaseModel


class ReleaseEmbedCacheKeyCriteria(BaseModel):
    ticket_id: str
    is_nsfw: bool
    lang: str

    def to_key_str(self):
        nsfw_str = "nsfw" if self.is_nsfw else "sfw"
        return f"{self.ticket_id}_{self.lang}_{nsfw_str}"


@dataclass
class ReleaseEmbedCache:
    key: ReleaseEmbedCacheKeyCriteria
    value: Sequence[Embed]
