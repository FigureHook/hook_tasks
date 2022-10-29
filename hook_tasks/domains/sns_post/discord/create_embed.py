from discord import Colour, Embed
from hook_tasks.domains.sns_post.models.release_ticket.model import ReleaseFeed

from .entities import ReleaseEmbed

__all__ = ("create_new_release_embed", "create_welcome_embed")

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
