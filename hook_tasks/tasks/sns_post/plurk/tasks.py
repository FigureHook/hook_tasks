import random
import time

from celery.utils.log import get_task_logger
from hook_tasks.api_clients import hook_api_client
from hook_tasks.app import app
from hook_tasks.domains.sns_post.plurk.create_plurk_usecase import (
    create_new_release_plurk_by_release_feed,
)
from hook_tasks.infras.persistance.release_ticket.release_ticket_repository import (
    ReleaseTicketRepository,
)
from hook_tasks.tasks.common.tasks import post_plurk
from hook_tasks.tasks.sns_post.common.tasks import create_release_ticket_for_purpose

logger = get_task_logger(__name__)


@app.task
def push_new_release_to_plurk():
    ticket = create_release_ticket_for_purpose.s("plurk_new_release").apply_async()
    ticket_id = ticket.get()

    if ticket_id:
        post_new_releases_to_plurk.s(ticket_id).apply_async()


@app.task
def post_new_releases_to_plurk(ticket_id: str) -> None:
    ticket_repo = ReleaseTicketRepository(hook_api_client)
    release_feeds = ticket_repo.get_release_feeds_by_ticket_id(ticket_id=ticket_id)

    for feed in release_feeds:
        plurk_model = create_new_release_plurk_by_release_feed(release_feed=feed)
        post_plurk.apply_async(args=(plurk_model.content, plurk_model.config.dict()))
        time.sleep(random.randint(5, 20))