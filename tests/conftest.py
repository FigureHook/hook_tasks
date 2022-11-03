from hook_tasks.domains.sns_post.common.value_objects.release_feed import ReleaseFeed
from pydantic_factories import ModelFactory
from pydantic_factories.plugins.pytest_plugin import register_fixture


@register_fixture
class ReleaseFeedFactory(ModelFactory):
    """ReleaseFeed factory"""

    __model__ = ReleaseFeed
