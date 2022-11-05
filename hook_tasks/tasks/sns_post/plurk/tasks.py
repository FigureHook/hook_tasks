import random
from typing import Any, Dict

from celery.utils.log import get_task_logger

from hook_tasks.api_clients import hook_api_client, plurk_api
from hook_tasks.app import app
from hook_tasks.domains.sns_post.common.use_cases.create_release_ticket_use_case import (
    CreateReleaseTicketUseCase,
)
from hook_tasks.domains.sns_post.plurk.create_plurk_usecase import (
    create_new_release_plurk_by_release_feed,
)
from hook_tasks.domains.sns_post.plurk.errors import (
    AntiFloodError,
    SameContent,
    TooManyNew,
)
from hook_tasks.domains.sns_post.plurk.use_cases.get_plurk_api_error_usecase import (
    GetPlurkApiErrorUserCase,
)
from hook_tasks.infras.persistance.release_ticket.release_ticket_repository import (
    ReleaseTicketRepository,
)

logger = get_task_logger(__name__)


@app.task(
    autoretry_for=(
        SameContent,
        TooManyNew,
    ),
    retry_backoff=300,
    max_retries=3,
    throws=(AntiFloodError,),
)
def post_plurk(self, content: str, config: Dict[str, Any]):
    options = {content: content, **config}
    resp = plurk_api.callAPI("/APP/Timeline/plurkAdd", options=options)
    if not resp:
        exc = GetPlurkApiErrorUserCase.get_add_plurk_error(error_body=plurk_api.error())
        raise exc

    return plurk_api.error


@app.task
def post_new_releases_to_plurk():
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
