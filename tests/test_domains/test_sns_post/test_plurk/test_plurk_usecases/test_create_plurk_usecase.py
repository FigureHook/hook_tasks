from hook_tasks.domains.sns_post.plurk.entities import (
    DOPlurkModel,
    PlurkConfig,
)

from hook_tasks.domains.sns_post.plurk.usecases.create_plurk import (
    create_new_release_plurk,
)


def test_create_new_release_plurk(release_feed_factory) -> None:
    release_feed = release_feed_factory.build()
    plurk_config = PlurkConfig(qualifier="shares")
    plurk_model = create_new_release_plurk(
        release_feed=release_feed, plurk_config=plurk_config
    )
    assert isinstance(plurk_model, DOPlurkModel)
