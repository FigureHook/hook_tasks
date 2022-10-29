import re
from datetime import date

import pytest
from discord import Embed
from hook_tasks.domains.sns_post.discord.create_embed_usecase import (
    EmbedLocale,
    ReleaseEmbed,
    create_new_release_embed,
    create_welcome_embed,
)
from hook_tasks.domains.sns_post.discord.localize_embed_usecase import (
    localize_release_embed_with_locale,
)
from hook_tasks.domains.sns_post.models.release_ticket.model import ReleaseFeed


class TestReleaseEmebed:
    @pytest.fixture
    def embed(
        self,
        release_feed_factory,
    ):
        release_feed: ReleaseFeed = release_feed_factory.build()
        return ReleaseEmbed(title=release_feed.name, url=release_feed.url)

    def test_set_nsfw(self, embed: ReleaseEmbed):
        assert not embed.is_nsfw
        embed.set_nsfw(is_nsfw=True)
        assert embed.is_nsfw

    def test_set_price(self, embed: ReleaseEmbed):
        embed.set_price(price=None)
        embed.set_price(price=12960)

    def test_set_release_date(self, embed: ReleaseEmbed):
        embed.set_release_date(release_date=None)
        embed.set_release_date(release_date=date(2222, 2, 2))

    def test_size(self, embed: ReleaseEmbed):
        embed.set_size(size=None)
        embed.set_size(size=250)

    def test_set_scale(self, embed: ReleaseEmbed):
        embed.set_scale(scale=None)
        embed.set_scale(scale=7)


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


def test_localize_release_embed(release_feed_factory):
    release_feed: ReleaseFeed = release_feed_factory.build(
        release_date=date(2022, 2, 2)
    )
    new_release_embed = create_new_release_embed(release_feed=release_feed)

    for locale in EmbedLocale:
        localized_embed = localize_release_embed_with_locale(
            release_embed=new_release_embed, locale=locale
        )
        assert isinstance(localized_embed, ReleaseEmbed)
