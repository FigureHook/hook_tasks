from datetime import date
from typing import Optional

from babel.dates import format_date
from hook_tasks.domains.sns_post.entities import ReleaseFeed
from hook_tasks.domains.sns_post.plurk.entities import (DOPlurkModel,
                                                        PlurkConfig)

from ..helpers import PlurkFormatHelper

__all__ = ("create_plurk", "create_new_release_plurk")


def create_plurk(content: str, plurk_config: PlurkConfig) -> DOPlurkModel:
    return DOPlurkModel(content=content, config=plurk_config)


def create_new_release_plurk(
    release_feed: ReleaseFeed, plurk_config: PlurkConfig
) -> DOPlurkModel:
    category_text = _get_category_text(release_feed.rerelease)
    post_header = _get_post_header_by_category(category_text)
    post_body = _get_post_body_by_release_feed(release_feed=release_feed)
    sep_line = _get_sep_line()
    ad_block = _get_ad_block()

    content = post_header + post_body + sep_line + ad_block

    return create_plurk(content=content, plurk_config=plurk_config)


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
