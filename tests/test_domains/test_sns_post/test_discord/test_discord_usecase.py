import re
from datetime import date

import pytest
from discord import Embed
from hook_tasks.domains.sns_post.discord.usecases.create_embed_usecase import (
    ReleaseEmbed,
    CreateEmbedUseCase,
)
from hook_tasks.domains.sns_post.discord.entities.webhook import DiscordWebhookLocale
from hook_tasks.domains.sns_post.common.value_objects.release_feed import ReleaseFeed
from hook_tasks.domains.sns_post.discord.usecases import (
    PreheatEmbedCacheUseCase,
    localize_release_embed_with_locale,
    MakeEmbedTrackableUseCase,
)
from hook_tasks.domains.sns_post.common.repositories.release_ticket_repository import (
    ReleaseTicketRepositoryInterface,
)
from hook_tasks.domains.sns_post.discord.repositories.release_embed_cache_repository import (
    ReleaseEmbedCacheRepositoryInterface,
)
from hook_tasks.domains.sns_post.discord.repositories.webhook_repository import (
    DiscordWebhookRepositoryInterface,
)


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
    welcome_embed = CreateEmbedUseCase.create_welcome_embed("Hello.")

    assert isinstance(welcome_embed, Embed)
    assert welcome_embed.title
    assert re.match(welcome_msg_pattern, welcome_embed.title)


def test_create_release_embed(release_feed_factory):
    release_feed: ReleaseFeed = release_feed_factory.build()
    new_release_embed = CreateEmbedUseCase.create_new_release_embed(
        release_feed=release_feed
    )

    assert isinstance(new_release_embed, ReleaseEmbed)


def test_localize_release_embed(release_feed_factory):
    release_feed: ReleaseFeed = release_feed_factory.build(
        release_date=date(2022, 2, 2)
    )
    new_release_embed = CreateEmbedUseCase.create_new_release_embed(
        release_feed=release_feed
    )

    for locale in DiscordWebhookLocale:
        localized_embed = localize_release_embed_with_locale(
            release_embed=new_release_embed, locale=locale
        )
        assert isinstance(localized_embed, ReleaseEmbed)


class TestTrackableEmbedUseCase:
    def test_tracable_by_ticket_id(self, release_feed_factory):
        release_feed: ReleaseFeed = release_feed_factory.build()
        ticket_id = "123"
        tracking_text_pattern = rf"ticket: {ticket_id}"
        release_embed = CreateEmbedUseCase.create_new_release_embed(
            release_feed=release_feed
        )
        release_embed = MakeEmbedTrackableUseCase.could_be_tracked_by_ticket_id(
            release_embed, ticket_id
        )
        assert release_embed.footer.text
        assert re.match(tracking_text_pattern, release_embed.footer.text)


class TestPreheatEmbedCacheUseCase:
    def test_process_cache_by_release_ticket_id(self, release_feed_factory):
        class MockCache(ReleaseEmbedCacheRepositoryInterface):
            def set_embed_cache(self, cache_key, embeds, ttl):
                pass

        class MockWebhookRepo(DiscordWebhookRepositoryInterface):
            def get_all_langs(self):
                return [
                    DiscordWebhookLocale.EN,
                    DiscordWebhookLocale.JA,
                    DiscordWebhookLocale.ZH_TW,
                ]

        class MockTicketRepo(ReleaseTicketRepositoryInterface):
            def get_release_feeds_by_ticket_id(self, ticket_id):
                return [release_feed_factory.build() for _ in range(10)]

        cache_usecase = PreheatEmbedCacheUseCase(
            ticket_repo=MockTicketRepo(),
            webhook_repo=MockWebhookRepo(),
            cache=MockCache(),
        )
        ticket_id = "123"
        assert ticket_id == cache_usecase.process_new_release_by_release_ticket_id(
            "123"
        )
