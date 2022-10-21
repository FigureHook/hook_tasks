from enum import IntEnum
from typing import List, Literal, Optional

from pydantic import BaseModel

PlurkQualifier = Literal[
    "plays",
    "buys",
    "sells",
    "loves",
    "likes",
    "shares",
    "hates",
    "wants",
    "wishes",
    "needs",
    "has",
    "will",
    "hopes",
    "asks",
    "wonders",
    "feels",
    "thinks",
    "draws",
    "is",
    "says",
    "eats",
    "writes",
    "whispers",
]

PlurkLang = Literal[
    "en",
    "tr_ch",
    "tr_hk",
    "cn",
    "ja",
    "ca",
    "el",
    "dk",
    "de",
    "es",
    "sv",
    "nb",
    "hi",
    "ro",
    "hr",
    "fr",
    "ru",
    "it",
    "he",
    "hu",
    "ne",
    "th",
    "ta_fp",
    "in",
    "pl",
    "ar",
    "fi",
    "tr",
    "ga",
    "sk",
    "uk",
    "fa",
    "pt_BR",
]


class PlurkCommentPermission(IntEnum):
    DEFAULT = 0
    NO_COMMENTS = 1
    ONLY_FRIENDS = 2


class PlurkConfig(BaseModel):
    qualifier: PlurkQualifier
    limited_to: List[int] = []
    excluded: Optional[List[int]] = None
    no_comments: PlurkCommentPermission = PlurkCommentPermission.DEFAULT
    lang: PlurkLang = "en"
    replurkable: bool = True
    porn: bool = False
    publish_to_fllowers: bool = True
    publish_to_anonymous: bool = True


class DOPlurkModel(BaseModel):
    content: str
    config: PlurkConfig
