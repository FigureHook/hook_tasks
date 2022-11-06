from hook_tasks.domains.sns_post.plurk.use_cases.create_plurk_use_case import (
    create_new_release_plurk_by_release_feed,
)
from hook_tasks.domains.sns_post.plurk.value_objects.plurk_model import PlurkModel


def test_create_new_release_plurk(release_feed_factory) -> None:
    release_feed = release_feed_factory.build()
    plurk_model = create_new_release_plurk_by_release_feed(release_feed=release_feed)
    assert isinstance(plurk_model, PlurkModel)
