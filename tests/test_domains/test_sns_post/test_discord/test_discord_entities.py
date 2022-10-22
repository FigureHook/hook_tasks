from hook_tasks.domains.sns_post.discord.entities import ReleaseEmbed
from hook_tasks.domains.sns_post.entities import ReleaseFeed


def test_release_embed_entity(release_feed_factory):
    release_feed: ReleaseFeed = release_feed_factory.build()

    embed = (
        ReleaseEmbed(
            title=release_feed.name,
            url=release_feed.url,
        )
        .set_nsfw(is_nsfw=release_feed.is_adult)
        .set_price(price=release_feed.price)
        .set_release_date(release_date=release_feed.release_date)
        .set_size(size=release_feed.size)
        .set_image(url=release_feed.media_image)
        .set_scale(scale=release_feed.scale)
    )

    assert embed.is_nsfw == release_feed.is_adult
