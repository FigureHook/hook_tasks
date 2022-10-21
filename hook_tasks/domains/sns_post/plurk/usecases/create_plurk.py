from babel.dates import format_date
from hook_tasks.domains.sns_post.entities import ReleaseFeed
from hook_tasks.domains.sns_post.plurk.entities import DOPlurkModel, PlurkConfig
from .helpers import PlurkFormatHelper


def create_plurk(content: str, plurk_config: PlurkConfig) -> DOPlurkModel:
    return DOPlurkModel(content=content, config=plurk_config)


def create_new_release_plurk(
    release_feed: ReleaseFeed, plurk_config: PlurkConfig
) -> DOPlurkModel:
    release_date_text, price_text = "未定", "未定"
    if release_feed.release_date:
        release_date_text = format_date(
            release_feed.release_date, "YYYY年 MMM", locale="zh"
        )

    if release_feed.price:
        price_text = f"{release_feed.price:,} 日圓"

    category_text = "再販" if release_feed.rerelease else "新品"

    post_category = PlurkFormatHelper.bold(f"[{category_text}速報]")
    post_product_name = PlurkFormatHelper.link(release_feed.name, release_feed.url)
    figure_hook_link = PlurkFormatHelper.link("Discord 速報訂閱", "https://bit.ly/3wj8Gpj")

    content = (
        ""
        f"{post_category}\n"
        f"商品名: {post_product_name}\n"
        f"作品名稱: {release_feed.series}\n"
        f"製造商: {release_feed.maker}\n"
        f"尺寸: {release_feed.size}mm(H)\n"
        f"發售日期: {release_date_text}\n"
        f"價格: {price_text}\n"
        f"{release_feed.media_image}\n"
        "----------\n"
        f"📨 {figure_hook_link}"
    )

    return create_plurk(content=content, plurk_config=plurk_config)
