from hook_tasks.domains.sns_post.models.release_ticket.model import ReleaseFeed
from pydantic_factories import ModelFactory
from pydantic_factories.plugins.pytest_plugin import register_fixture


@register_fixture
class ReleaseFeedFactory(ModelFactory):
    """ReleaseFeed factory"""

    __model__ = ReleaseFeed
