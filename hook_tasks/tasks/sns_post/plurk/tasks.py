import random

from celery.utils.log import get_task_logger

from hook_tasks.api_clients import hook_api_client
from hook_tasks.app import app
from hook_tasks.domains.sns_post.common.use_cases.create_release_ticket_use_case import (
    CreateReleaseTicketUseCase,
)
from hook_tasks.domains.sns_post.plurk.create_plurk_usecase import (
    create_new_release_plurk_by_release_feed,
)
from hook_tasks.infras.persistance.release_ticket.release_ticket_repository import (
    ReleaseTicketRepository,
)

from ..common.tasks import post_plurk

logger = get_task_logger(__name__)


@app.task
def post_new_releases_to_plurk(ticket_id: str):
    ticket_repo = ReleaseTicketRepository(hook_api_client)
    ticket_use_case = CreateReleaseTicketUseCase(ticket_repo=ticket_repo)

    ticket_id = ticket_use_case.create_release_ticket_for_purpose("plurk_new_release")
    release_feeds = ticket_repo.get_release_feeds_by_ticket_id(ticket_id=ticket_id)

    next_countdown = 0
    for feed in release_feeds:
        plurk_model = create_new_release_plurk_by_release_feed(release_feed=feed)
        post_plurk.s(plurk_model.content, plurk_model.config.dict()).apply_async(
            count_down=next_countdown
        )
        next_countdown += random.randint(10, 30)
