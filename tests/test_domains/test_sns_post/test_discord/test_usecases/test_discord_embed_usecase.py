import re

from discord import Embed
from hook_tasks.domains.sns_post.discord.entities import (EmbedLocale,
                                                          ReleaseEmbed)
from hook_tasks.domains.sns_post.discord.usecases.create_embed import (
    create_new_release_embed, create_welcome_embed)
from hook_tasks.domains.sns_post.discord.usecases.localize_embed import \
    localize_release_embed_with_locale
from hook_tasks.domains.sns_post.entitles import ReleaseFeed


def test_create_welcom_embed():
    welcome_msg_pattern = r":hook: (.+) :hook:"
    welcome_embed = create_welcome_embed("Hello.")

    assert isinstance(welcome_embed, Embed)
    assert welcome_embed.title
    assert re.match(welcome_msg_pattern, welcome_embed.title)


def test_create_release_embed(release_feed_factory):
    release_feed: ReleaseFeed = release_feed_factory.build()
    new_release_embed = create_new_release_embed(release_feed=release_feed)

    assert isinstance(new_release_embed, ReleaseEmbed)


def test_locaolize_release_embed(release_feed_factory):
    release_feed: ReleaseFeed = release_feed_factory.build()
    new_release_embed = create_new_release_embed(release_feed=release_feed)

    for locale in EmbedLocale:
        localized_embed = localize_release_embed_with_locale(
            release_embed=new_release_embed, locale=locale
        )
        assert not localized_embed.is_raw
