from copy import deepcopy
from datetime import date
from enum import Enum
from typing import Any, Optional

from typing_extensions import Self

from discord import Colour, Embed


class StrEnum(str, Enum):
    ...


class EmbedLocale(StrEnum):
    ZH_TW = "zh-TW"
    EN = "en"
    JA = "ja"


class ReleaseEmbed(Embed):
    _is_nsfw: bool

    def __init__(self, *, title: str, url: str):
        self._is_nsfw = False
        super().__init__(colour=Colour.red(), title=title, url=url)

    @property
    def is_nsfw(self):
        return self._is_nsfw

    def copy(self):
        return deepcopy(super().copy())

    def add_field(self, *, name: str, value: Any, inline: bool = True):
        if not value:
            return self
        return super().add_field(name=name, value=value, inline=inline)

    def set_price(self, *, price: Optional[int]) -> Self:
        if price:
            self.add_field(name="price", value=f"JPY {price:,}", inline=True)
        return self

    def set_release_date(self, *, release_date: Optional[date]) -> Self:
        self.add_field(name="release_date", value=release_date, inline=True)
        return self

    def set_size(self, *, size: Optional[int]) -> Self:
        if size:
            self.add_field(name="size", value=f"{size} mm", inline=True)
        return self

    def set_scale(self, *, scale: Optional[int]) -> Self:
        if scale:
            self.add_field(name="scale", value=f"1/{scale}", inline=True)
        return self

    def set_nsfw(self, *, is_nsfw: bool) -> Self:
        self._is_nsfw = is_nsfw
        return self
