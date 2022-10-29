from datetime import date, datetime
from typing import TYPE_CHECKING

from babel.dates import format_date

from .create_embed_usecase import EmbedLocale, ReleaseEmbed

if TYPE_CHECKING:
    from discord.embeds import _EmbedFieldProxy

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


def localize_release_embed_with_locale(
    release_embed: ReleaseEmbed, locale: EmbedLocale
) -> ReleaseEmbed:
    embed = release_embed.copy()
    embed_locale = embed_templates[locale]

    if embed.author:
        if embed.author.name:
            author_name = embed_locale.get(embed.author.name)
            embed.set_author(name=author_name, icon_url=embed.author.icon_url)

    for field in embed.fields:
        field_raw_name = field.name
        field = _localize_field_name_with_locale(
            field=field, translation_map=embed_locale
        )
        if field_raw_name == "release_date":
            field = _localize_release_date_field_value_with_locale(
                release_date_field=field, locale=locale
            )

    return embed


def _localize_field_name_with_locale(
    field: "_EmbedFieldProxy", translation_map: dict[str, str]
) -> "_EmbedFieldProxy":
    if field.name:
        field.name = translation_map.get(field.name, field.name)
    return field


def _localize_release_date_field_value_with_locale(
    release_date_field: "_EmbedFieldProxy",
    locale: EmbedLocale,
) -> "_EmbedFieldProxy":
    if release_date_field.value:
        release_date = datetime.strptime(release_date_field.value, "%Y-%m-%d").date()
        release_date_field.value = _get_localized_release_date_text(
            release_date, locale=locale
        )
    return release_date_field


def _get_localized_release_date_text(release_date: date, locale: EmbedLocale) -> str:
    babel_locale = locale_mapping.get(locale, "en")
    date_format = embed_templates[locale]["date_format"]
    return format_date(release_date, date_format, locale=babel_locale)
