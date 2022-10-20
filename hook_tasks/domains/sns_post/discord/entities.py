from copy import deepcopy
from enum import Enum

from discord import Colour, Embed


class StrEnum(str, Enum):
    ...


class EmbedLocale(StrEnum):
    ZH_TW = "zh-TW"
    EN = "en"
    JA = "ja"


class ReleaseEmbed(Embed):
    _is_nsfw: bool
    _is_raw: bool

    def __init__(self, **kwargs):
        kwargs.setdefault("colour", Colour.red())
        self._is_raw = True
        self._is_nsfw = kwargs.pop("is_nsfw", False)
        super().__init__(**kwargs)

    @property
    def is_nsfw(self):
        return self._is_nsfw

    @property
    def is_raw(self):
        return self._is_raw

    def confirm_localized(self):
        self._is_raw = False

    def copy(self):
        return deepcopy(super().copy())

    def add_field(self, *, name, value, inline):
        if not value:
            return self
        return super().add_field(name=name, value=value, inline=inline)
