from enum import Enum

from pydantic import BaseModel


class StrEnum(str, Enum):
    ...


class DiscordWebhookLocale(StrEnum):
    ZH_TW = "zh-TW"
    EN = "en"
    JA = "ja"


class DiscordWebhook(BaseModel):
    id: str
    token: str
    lang: DiscordWebhookLocale
    locale: DiscordWebhookLocale
    channel_id: str
    is_nsfw: bool
    is_existed: bool
