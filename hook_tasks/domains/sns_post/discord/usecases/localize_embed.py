from datetime import datetime
from typing import Any

from babel.dates import format_date
from discord import Embed

from ..entities import EmbedLocale, ReleaseEmbed

embed_templates = {
    EmbedLocale.EN: {
        "maker": "Manufacturer",
        "series": "Series",
        "price": "Price",
        "release_date": "Release Date",
        "sculptors": "Sculptors",
        "paintworks": "Paintworks",
        "date_format": "MMM, yyyy",
        "size": "Size",
        "scale": "Scale",
        "new_release": "New Release",
        "re_release": "Rerelease",
    },
    EmbedLocale.JA: {
        "maker": "メーカー",
        "series": "作品名",
        "price": "価格",
        "release_date": "発売時期",
        "sculptors": "原型制作",
        "paintworks": "彩色",
        "date_format": "yyyy年 MMM",
        "size": "サイズ",
        "scale": "スケール",
        "new_release": "新リリース",
        "re_release": "新リリース（再販）",
    },
    EmbedLocale.ZH_TW: {
        "maker": "製造商",
        "series": "作品名稱",
        "price": "價格",
        "release_date": "發售日期",
        "sculptors": "原型製作",
        "paintworks": "色彩",
        "date_format": "yyyy年 MMM",
        "size": "尺寸",
        "scale": "比例",
        "new_release": "新商品",
        "re_release": "新商品(再販)",
    },
}

locale_mapping = {
    EmbedLocale.EN: "en",
    EmbedLocale.JA: "ja",
    EmbedLocale.ZH_TW: "zh",
}


def localize_release_embed_to_embed_with_locale(
    release_embed: ReleaseEmbed, locale: EmbedLocale
) -> Embed:
    embed = release_embed.copy()
    embed_locale = embed_templates[locale]

    if embed.author:
        key = str(embed.author.name)
        author_name = embed_locale.get(key)
        embed.set_author(name=author_name, icon_url=embed.author.icon_url)

    for field in embed._fields:
        key = field["name"]
        field["name"] = embed_locale.get(key, key)

        if key == "release_date":
            _localize_release_date_field_with_locale(
                release_date_filed=field, locale=locale
            )

    return Embed.from_dict(embed.to_dict())


def _localize_release_date_field_with_locale(
    release_date_filed: dict[str, Any],
    locale: EmbedLocale,
):
    babel_locale = locale_mapping.get(locale, "en")
    date_format = embed_templates[locale]["date_format"]
    if release_date_filed["value"]:
        release_date = datetime.strptime(release_date_filed["value"], "%Y-%m-%d").date()
        release_date_filed["value"] = str(
            format_date(release_date, date_format, locale=babel_locale)
        )
