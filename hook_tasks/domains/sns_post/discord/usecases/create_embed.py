from discord import Colour, Embed
from hook_tasks.domains.sns_post.entitles import ReleaseFeed

from ..entities import ReleaseEmbed


def create_new_release_embed(release_feed: ReleaseFeed) -> ReleaseEmbed:
    embed = ReleaseEmbed(
        title=release_feed.name,
        type="rich",
        url=release_feed.url,
        is_nsfw=release_feed.is_adult,
    )

    author = "re_release" if release_feed.rerelease else "new_release"

    embed.set_image(url=release_feed.media_image).set_author(
        name=author,
        # Icons made by Pixel perfect from www.flaticon.com
        icon_url="https://image.flaticon.com/icons/png/32/879/879833.png",  # type: ignore
    ).add_field(name="maker", value=release_feed.maker, inline=False).add_field(
        name="series", value=release_feed.series, inline=False
    )

    if release_feed.thumbnail:
        embed.set_thumbnail(url=release_feed.thumbnail)

    if release_feed.size:
        embed.add_field(name="size", value=f"{release_feed.size} mm", inline=True)

    # if scale:
    #     embed.add_field(
    #         name="scale", value=f"1/{scale}", inline=True
    #     )

    embed.add_field(
        name="release_date", value=release_feed.release_date, inline=True
    )

    if release_feed.price:
        embed.add_field(
            name="price", value=f"JPY {release_feed.price:,}", inline=True
        )

    return embed

def create_welcome_embed(msg: str) -> Embed:
    title = f":hook: {msg} :hook:"
    embed = Embed(title=title, colour=Colour(0x00B5FF))
    return embed
