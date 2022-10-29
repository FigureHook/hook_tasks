from datetime import date

import pytest
from hook_tasks.domains.sns_post.discord.entities import ReleaseEmbed
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
