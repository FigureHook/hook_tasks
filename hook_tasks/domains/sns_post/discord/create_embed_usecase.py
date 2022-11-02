from copy import deepcopy
from datetime import date
from typing import Any, Optional

from hook_tasks.domains.sns_post.common.value_objects.release_feed import ReleaseFeed
from typing_extensions import Self

from discord import Colour, Embed


class ReleaseEmbed(Embed):
    _is_nsfw: bool

    def __init__(self, *, title: str, url: str):
        self._is_nsfw = False
        super().__init__(colour=Colour.red(), title=title, url=url)

    @property
    def is_nsfw(self):
        return self._is_nsfw

    def copy(self) -> Self:
        return deepcopy(super().copy())

    def add_field(self, *, name: str, value: Any, inline: bool = True) -> Self:
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


NEW_RELEASE_ICON_URL = "https://images.figurehook.com/icons/new_by_flaticon.png"
WELCOME_EMBED_THEME_COLOR = Colour(0x00B5FF)


def create_new_release_embed(release_feed: ReleaseFeed) -> ReleaseEmbed:
    info_category = "re_release" if release_feed.rerelease else "new_release"
    embed = (
        ReleaseEmbed(
            title=release_feed.name,
            url=release_feed.url,
        )
        .set_author(
            name=info_category,
            icon_url=NEW_RELEASE_ICON_URL,
        )
        .set_nsfw(is_nsfw=release_feed.is_adult)
        .set_price(price=release_feed.price)
        .set_release_date(release_date=release_feed.release_date)
        .set_size(size=release_feed.size)
        .set_thumbnail(url=release_feed.thumbnail)
        .set_image(url=release_feed.media_image)
        .add_field(name="maker", value=release_feed.maker, inline=False)
        .add_field(name="series", value=release_feed.series, inline=False)
        .set_scale(scale=release_feed.scale)
    )
    return embed


def create_welcome_embed(msg: str) -> Embed:
    title = f":hook: {msg} :hook:"
    embed = Embed(title=title, colour=WELCOME_EMBED_THEME_COLOR)
    return embed
