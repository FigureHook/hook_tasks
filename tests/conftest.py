import os
import shutil
from urllib.parse import urlparse
from urllib.request import url2pathname

import pytest
from pydantic_factories import ModelFactory
from pydantic_factories.plugins.pytest_plugin import register_fixture

os.environ["ENV"] = "test"


from hook_tasks.app import app  # noqa: E402
from hook_tasks.domains.sns_post.common.value_objects.release_feed import (  # noqa: E402
    ReleaseFeed,
)


@pytest.fixture
def celery_app(celery_app):
    yield app
    if "file:///" in app.conf.result_backend:
        shutil.rmtree(url2pathname(urlparse(app.conf.result_backend).path))


# @pytest.fixture
# def celery_worker_parameters():
#     # type: () -> Mapping[str, Any]
#     """Redefine this fixture to change the init parameters of Celery workers.

#     This can be used e. g. to define queues the worker will consume tasks from.

#     The dict returned by your fixture will then be used
#     as parameters when instantiating :class:`~celery.worker.WorkController`.
#     """
#     return {
#         # For some reason this `celery.ping` is not registed IF our own worker is still
#         # running. To avoid failing tests in that case, we disable the ping check.
#         # see: https://github.com/celery/celery/issues/3642#issuecomment-369057682
#         # here is the ping task: `from celery.contrib.testing.tasks import ping`
#         "perform_ping_check": False,
#     }


@register_fixture
class ReleaseFeedFactory(ModelFactory):
    """ReleaseFeed factory"""

    __model__ = ReleaseFeed
