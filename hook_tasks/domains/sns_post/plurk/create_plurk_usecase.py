from datetime import date
from enum import IntEnum
from typing import List, Literal, Optional

from babel.dates import format_date
from hook_tasks.domains.sns_post.models.release_ticket.model import ReleaseFeed
from pydantic import BaseModel

from .format_helper import PlurkFormatHelper

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

    def to_plurk_config(self):
        return {"content": self.content, **self.config.dict()}


def create_plurk(content: str, plurk_config: PlurkConfig) -> DOPlurkModel:
    return DOPlurkModel(content=content, config=plurk_config)


def create_new_release_plurk_by_release_feed(release_feed: ReleaseFeed) -> DOPlurkModel:
    category_text = _get_category_text(release_feed.rerelease)
    post_header = _get_post_header_by_category(category_text)
    post_body = _get_post_body_by_release_feed(release_feed=release_feed)
    sep_line = _get_sep_line()
    ad_block = _get_ad_block()

    content = post_header + post_body + sep_line + ad_block

    return create_plurk(
        content=content,
        plurk_config=PlurkConfig(
            qualifier="shares", porn=release_feed.is_adult, lang="tr_ch"
        ),
    )


UNKNOWN_TEXT = "未定"


def _get_post_header_by_category(category: str) -> str:
    return PlurkFormatHelper.bold(f"[{category}速報]") + "\n"


def _get_post_body_by_release_feed(release_feed: ReleaseFeed) -> str:
    post_product_name = _get_linkable_product_name(release_feed.name, release_feed.url)
    price_text = _get_price_text(release_feed.price)
    release_date_text = _get_release_date_text(release_feed.release_date)

    return (
        f"商品名: {post_product_name}\n"
        f"作品名稱: {release_feed.series}\n"
        f"製造商: {release_feed.maker}\n"
        f"尺寸: {release_feed.size}mm(H)\n"
        f"發售日期: {release_date_text}\n"
        f"價格: {price_text}\n"
        f"{release_feed.media_image}\n"
    )


def _get_ad_block() -> str:
    figure_hook_link = PlurkFormatHelper.link("Discord 速報訂閱", "https://bit.ly/3wj8Gpj")
    return f"📨 {figure_hook_link}"


def _get_linkable_product_name(product_name: str, url: str) -> str:
    return PlurkFormatHelper.link(product_name, url)


def _get_release_date_text(release_date: Optional[date]) -> str:
    return (
        format_date(release_date, "YYYY年 MMM", locale="zh")
        if release_date
        else UNKNOWN_TEXT
    )


def _get_price_text(price: Optional[int]) -> str:
    return f"{price:,} 日圓" if price else UNKNOWN_TEXT


def _get_category_text(is_rerelease: bool) -> str:
    return "再販" if is_rerelease else "新品"


def _get_sep_line() -> str:
    return "----------\n"
